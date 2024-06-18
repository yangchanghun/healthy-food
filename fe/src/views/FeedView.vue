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
        <div class="main-center col-span-3 grid grid-cols-3 gap-4" ref="content">
            <RouterLink :to="{name:'postview', params: {id: post.id}}" 
                class="space-y-4" 
                v-for="post in displayedPosts" 
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
            otherPosts: [], // 모든 포스트 데이터를 담을 배열
            displayedPosts: [], // 화면에 보여줄 포스트 데이터를 담을 배열
            loadedPostCount: 0, // 로드된 포스트의 수
            page: 1,
            perPage: 9,
            category: 'all',
        }
    },

    mounted() {
        this.getFeed('all');
        window.addEventListener('scroll', this.handleScroll);
    },

    destroyed() {
        // 컴포넌트 소멸 시 이벤트 리스너 제거
        window.removeEventListener('scroll', this.handleScroll);
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
                    this.otherPosts = response.data; // 전체 포스트 데이터를 저장
                    this.resetDisplayedPosts(); // 카테고리 변경 시 초기 포스트 로딩
                })
                .catch(error => {
                    console.log('error', error)
                })
        },
        categorizeProduct(category) {
            this.category = category;
            this.page = 1; // 페이지 초기화
            this.loadedPostCount = 0; // 로드된 포스트 수 초기화
            this.getFeed(category);
        },
        loadMorePosts() {
            const remainingPosts = this.otherPosts.slice(
                this.loadedPostCount,
                this.loadedPostCount + this.perPage
            );
            this.displayedPosts = [...this.displayedPosts, ...remainingPosts];
            this.loadedPostCount += this.perPage;
        },
        resetDisplayedPosts() {
            this.displayedPosts = [];
            this.loadMorePosts();
        },
        // 스크롤 이벤트 핸들러
        handleScroll() {
            const contentHeight = this.$refs.content.offsetHeight;
            const yOffset = window.scrollY;
            const windowHeight = window.innerHeight;
            if (yOffset + windowHeight >= contentHeight) {
                this.loadMorePosts();
            }
        },
    }
}
</script>
