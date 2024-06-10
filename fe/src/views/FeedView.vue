<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
      <div class="main-center col-span-3 grid grid-cols-3 gap-4" ref="content">
        <RouterLink
          :to="{ name: 'postview', params: { id: post.id } }"
          class="space-y-4"
          v-for="post in displayedPosts"
          :key="post.id"
        >
          <FeedListItem :post="post" />
        </RouterLink>
      </div>
  
      <div class="main-right col-span-1 space-y-4">
        <Trends />
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import Trends from '../components/Trends.vue';
  import FeedListItem from '../components/FeedListItem.vue';
  
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

      };
    },
  
    mounted() {
      this.getFeed();
      window.addEventListener('scroll', this.handleScroll);
    },
  
    destroyed() {
      // 컴포넌트 소멸 시 이벤트 리스너 제거
      window.removeEventListener('scroll', this.handleScroll);
    },
  
    methods: {
      getFeed() {
        axios
          .get('/api/posts/')
          .then(response => {
            console.log('data', response.data);
  
            this.otherPosts = response.data; // 전체 포스트 데이터를 저장
            this.loadMorePosts(); // 초기에 화면에 보여줄 포스트 로딩
          })
          .catch(error => {
            console.log('error', error);
          });
      },
      loadMorePosts() {
        const remainingPosts = this.otherPosts.slice(
          this.loadedPostCount,
          this.loadedPostCount + this.perPage
        );
        this.displayedPosts = [...this.displayedPosts, ...remainingPosts];
        this.loadedPostCount += this.perPage;
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
    },
  };
  </script>