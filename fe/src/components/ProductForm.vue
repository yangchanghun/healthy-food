<template>
    <form v-on:submit.prevent="submitForm" method="post">
        <div class="p-4">
            <select v-model="category" class="p-4 w-full bg-gray-100 rounded-lg mt-2">
                <option value="" disabled>Category</option>
                <option value="fruit">과일</option>
                <option value="vegetable">채소</option>
            </select>            
            <input v-model="price" type="text" placeholder="가격" class="p-4 w-full bg-gray-100 rounded-lg mt-2" />
            <input v-model="name" type="text" placeholder="상품명 EX) 복숭아" class="p-4 w-full bg-gray-100 rounded-lg mt-2" />
            <input v-model="specific" type="text" placeholder="상품 상세정보 EX) 딱딱이 복숭아 1.5kg" class="p-4 w-full bg-gray-100 rounded-lg mt-2" />
            <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg mt-4" placeholder="본문 내용 EX) 복숭아는 맛있어요"></textarea>

            <div id="preview" v-if="urls.length">
                <img v-for="(url, index) in urls" :key="index" :src="url" class="w-[100px] mt-3 rounded-xl" />
            </div>
        </div>

        <div class="p-4 border-t border-gray-100 flex justify-between">
            <label class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">
                <input type="file" ref="file" @change="onFileChange" multiple>
                Attach images
            </label>
            <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Post</button>
        </div>
    </form>
</template>

<script>
import axios from 'axios'

export default {
    data() {
        return {
            body: '',
            category: '',
            price: '',
            name: '',
            specific: '',
            urls: [],
        }
    },

    methods: {
        onFileChange(e) {
            const files = e.target.files;
            this.urls = Array.from(files).map(file => URL.createObjectURL(file)); 
        },
        
        submitForm() {
            console.log('submitForm', this.body, this.category, this.price, this.name, this.specific)
            
            let formData = new FormData();
            Array.from(this.$refs.file.files).forEach(file => {
                formData.append('images', file);
            });
            formData.append('body', this.body);
            formData.append('category', this.category);
            formData.append('price', this.price);
            formData.append('name', this.name);
            formData.append('specific', this.specific);

            axios
                .post('/api/posts/create/product/', formData, {
                    headers: {
                        "Content-Type": "multipart/form-data"
                    }
                })
                .then(response => {
                    console.log('data', response.data)

                    this.body = ''
                    this.category = ''
                    this.price = ''
                    this.name = ''
                    this.specific = ''
                    this.$refs.file.value = null
                    this.urls = []
                    window.location.reload()

                })
                .catch(error => {
                    console.log('error', error)
                })
        },
    }
}
</script>