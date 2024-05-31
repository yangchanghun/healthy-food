<template>
    <div class="image-grid">
        <template v-if="post.attachments.length">
            <img 
                :src="post.attachments[0].get_image" 
                class="image-item  mb-4 rounded-xl transition-transform duration-500 hover:scale-105"
                style="width: 500px; height: 300px; object-fit: cover;"
            
            >
        </template>
    </div>
</template>

<script>
export default {
    props: {
        post: Object
    },
}
</script>