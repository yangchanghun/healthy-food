<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        
        <div class="main-left col-span-1">
            <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
                <img src="https://i.pravatar.cc/300?img=70" class="mb-6 rounded-full">
                
                <p><strong>{{ user.name }}</strong></p>

                <div class="mt-6 flex space-x-8 justify-around">
                    <p class="text-xs text-gray-500"> {{ user.followers_count }} followers</p>
                    <p class="text-xs text-gray-500"> {{ user.following_count }} following</p>
                    <p class="text-xs text-gray-500">120 posts</p>
                </div>

                <div class="mt-6">
                    <button 
                        class="inline-block py-4 px-3 bg-blue-600 text-xs text-white rounded-lg" 
                        @click="sendFollow"
                        v-if="!isFollowing && userStore.user.id !== user.id"
                    >
                        Follow
                    </button>
                    <button 
                        class="inline-block py-4 px-3 bg-gray-600 text-xs text-white rounded-lg" 
                        @click="sendFollow"
                        v-else-if="isFollowing && userStore.user.id !== user.id"
                    >
                        Unfollow
                    </button>
                
                    <button 
                        class="inline-block py-4 px-3 bg-red-600 text-xs text-white rounded-lg" 
                        @click="logout"
                        v-if="userStore.user.id === user.id"
                    >
                        Log out
                    </button>
                </div>


            </div>
        </div>

        <div class="main-center col-span-2 space-y-4">
            <div 
                class="bg-white border border-gray-200 rounded-lg"
                v-if="userStore.user.id === user.id"
            >
                <form v-on:submit.prevent="submitForm" method="post">
                    <div class="p-4">  
                        <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="What are you thinking about?"></textarea>
                    </div>

                    <div class="p-4 border-t border-gray-100 flex justify-between">
                        <a href="#" class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">Attach image</a>

                        <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Post</button>
                    </div>
                </form>
            </div>

            <div 
                class="p-4 bg-white border border-gray-200 rounded-lg"
                v-for="post in posts"
                v-bind:key="post.id"
            >
                <FeedItem v-bind:post="post" />
            </div>
        </div>

        <div class="main-right col-span-1 space-y-4">
            <PeopleYouMayKnow />

            <Trends />
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue'
import Trends from '../components/Trends.vue'
import FeedItem from '../components/FeedItem.vue'
import { useUserStore } from '@/stores/user'

export default {
    name: 'FeedView',

    created() {
    this.checkFollowStatus();
    },

    setup() {
        const userStore = useUserStore()

        return {
            userStore
        }
    },

    components: {
        PeopleYouMayKnow,
        Trends,
        FeedItem
    },

    data() {
        return {
            posts: [],
            user: {},
            body: '',
            isFollowing: false,
        }
    },

    mounted() {
        this.getFeed()
    },

    watch: { 
        '$route.params.id': {
            handler: function() {
                this.getFeed()
            },
            deep: true,
            immediate: true
        }
    },

    methods: {

        // 사용자가 현재 페이지의 프로필을 팔로우하고 있는지 확인하는 API 호출
        checkFollowStatus() {
        axios.post(`/api/follow/${this.$route.params.id}/status/`)
            .then(response => {
                this.isFollowing = response.data.isFollowing;
            })
            .catch(error => {
                console.error('Follow status check error', error);
            });
    },

        sendFollow() {
            axios
                .post(`/api/follow/${this.$route.params.id}/request/`)
                .then(response => {
                    console.log('data', response.data)

                    if (response.data.message === 'unfollow') {
                        this.isFollowing = false;
                        this.user.followers_count -= 1
                    } else {
                        this.isFollowing = true;
                        this.user.followers_count += 1
                    }
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        getFeed() {
            axios
                .get(`/api/posts/profile/${this.$route.params.id}/`)
                .then(response => {
                    console.log('data', response.data)

                    this.posts = response.data.posts
                    this.user = response.data.user
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        submitForm() {
            console.log('submitForm', this.body)

            axios
                .post('/api/posts/create/', {
                    'body': this.body
                })
                .then(response => {
                    console.log('data', response.data)

                    this.posts.unshift(response.data)
                    this.body = ''
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        logout() {
            console.log('Log out')

            this.userStore.removeToken()

            this.$router.push('/login')
        }
    }
}
</script>