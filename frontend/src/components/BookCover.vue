<script setup>
import { RouterLink } from 'vue-router';
import { defineProps } from "vue"
import { ref, onUpdated } from 'vue'


const props = defineProps(["book", "token", "authorisation"])

</script>

<template>
    
        <div class="post">
            <table style="margin: auto;">

                <tr>
                    <td style="font-size: large;font-weight: bolder;">
                        <h2>{{ book.Name }}</h2>
                    </td>
                </tr>
                <tr>
                    <td style="color: gray;">
                        {{ book.Author }}
                    </td>
                </tr>
                <tr v-if="authorisation='admin'">
                    <td style="padding-top:0px;font-size:15px;">
                        <button @click.stop.prevent class="new">
                            Edit Book
                        </button>
                        <button @click.stop.prevent class="new">
                            Delete Book
                        </button>
                    </td>
                </tr>
            </table>
        </div>

    
</template>