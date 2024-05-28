
<template>
    <form v-on:submit.prevent="submitForm" method="post">
    <div class="p-4">  
        <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="What are you thinking about?"></textarea>

        <div id="preview" v-if="url">
            <img :src="url" class="w-[100px] mt-3 rounded-xl" />
        </div>
    </div>

    <div class="p-4 border-t border-gray-100 flex justify-between">
        <label class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">
            <input type="file" ref="file" @change="onFileChange">
            Attach image
        </label>
        <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Post</button>
    </div>
    </form>
</template>


<script>
import axios from 'axios'

export default {
    props: {
        user: Object,
        posts: Array
    },

    data() {
        return {
            body: '',
            url: null,
        }
    },

    methods: {
        // 미리보기
        onFileChange(e) {
            const file = e.target.files[0];
            this.url = URL.createObjectURL(file);
        },
        
        submitForm() {
            console.log('submitForm', this.body)
            
            let formData = new FormData()
            formData.append('image', this.$refs.file.files[0])
            formData.append('body', this.body)

            axios
                .post('/api/posts/create/', formData,{
                    headers: {
                        "Content-Type": "multipart/form-data"
                    }
                })
                .then(response => {
                    console.log('data', response.data)

                    this.posts.unshift(response.data)
                    this.body = ''
                    this.$refs.file.value = null
                    this.url = null
                })
                .catch(error => {
                    console.log('error', error)
                })
        },
    }
}
</script>

