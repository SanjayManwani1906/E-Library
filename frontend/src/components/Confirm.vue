<script setup>

import { ref } from 'vue'
import { defineProps, defineEmits } from "vue"

const props = defineProps(["post","token"])
const emits = defineEmits(["close","delete","archive"])

</script>

<template>
    <div align='center'>
        <div 
        style="border:1px grey solid;border-radius:20px;width:300px;padding:10px; background-color: black;">
            <p style="color: antiquewhite; font-size: 15px;">
                Are you sure you want to delete <br> {{ post.Title }} ?
            </p>
            <div style="display: flex; justify-content: space-evenly; margin-top: 5px;">
                <button @click="$emit('archive')" class="new">Archive Instead</button>
                <button @click="$emit('delete')" class="new" style="color: red;">Delete Post</button>
            </div>
            
            <button @click="$emit('close')" class="new" style="margin-top: 10px;">Close</button>
        </div>
    </div>
</template>