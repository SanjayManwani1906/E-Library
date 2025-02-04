<script setup>

import { defineProps } from "vue"
import { ref, onUpdated} from 'vue'


const props = defineProps(["chapter"])
const content = ref(undefined)
onUpdated(()=>{
    content.value = "<link href='/src/assets/content.css' rel='stylesheet' type='text/css' />"+
        "<h2 align='center'>" + props.chapter.Title + "</h2>" +
        "<pre>" + props.chapter.Content + "</pre>" +
        "<meta name='color-scheme' content='light dark'>" 
        
})



</script>
<template>
    <main>
        <div style="display:flex; justify-content: space-evenly;flex-wrap:wrap;align-items: center;">
            <div style="padding:10px;">
                <img :src="chapter.ChapterImage" class="post-image" style="max-height:425px">
            </div>
            <div style="display:flex;flex-grow: 1;">
                <iframe style="margin:5px" frameborder="0" height=500px :srcdoc="content"></iframe>
            </div>
        </div>
    </main>
</template>