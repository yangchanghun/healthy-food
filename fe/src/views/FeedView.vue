<template>
    <div class="mx-20 mt-2 mb-6">
        <button @click="categorizeProduct('all')" 
                :class="['mx-1 px-4 py-2 rounded text-white', category === 'all' ? 'bg-blue-600' : 'bg-blue-500 hover:bg-blue-600']">전체</button>
        <button @click="categorizeProduct('fruit')" 
                :class="['mx-1 px-4 py-2 rounded text-white', category === 'fruit' ? 'bg-blue-600' : 'bg-blue-500 hover:bg-blue-600']">과일</button>
        <button @click="categorizeProduct('vegetable')" 
                :class="['mx-1 px-4 py-2 rounded text-white', category === 'vegetable' ? 'bg-blue-600' : 'bg-blue-500 hover:bg-blue-600']">채소</button>
    </div>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">

        <div class="main-center col-span-3 grid grid-cols-3 gap-4">
            <RouterLink :to="{name:'postview', params: {id: post.id}}" 
                class="space-y-4" 
                v-for="post in posts" 
                v-bind:key="post.id"
            >
                <FeedListItem v-bind:post="post" />
            </RouterLink>
        </div>

        <div class="main-right col-span-1 space-y-4">

            <Trends />
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import Trends from '../components/Trends.vue'
import FeedListItem from '../components/FeedListItem.vue'

export default {
    name: 'FeedView',

    components: {
        Trends,
        FeedListItem,
    },

    data() {
        return {
            posts: [],
            body: '',
            category: 'all',
        }
    },

    mounted() {
        this.getFeed('all')
    },

    methods: {
        getFeed(category) {
            let url = '/api/posts/';
            if (category !== 'all') {
                url += `?category=${category}`;
            }

            axios
                .get(url)
                .then(response => {
                    console.log('data', response.data)

                    this.posts = response.data
                })
                .catch(error => {
                    console.log('error', error)
                })
        },
        categorizeProduct(category) {
            this.category = category
            this.getFeed(category)
        }
    }
}
</script>
