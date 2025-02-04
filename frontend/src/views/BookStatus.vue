<script setup>

import { RouterLink } from 'vue-router';
import { useRoute } from 'vue-router'
import { onBeforeMount, onMounted, ref, watch } from 'vue'
import BookCover from '../components/BookCover.vue'


const route = useRoute()
const book = ref("")
const mybook = ref([])
const feedback = ref([])
const admin = ref('admin')


function data() {
    fetch("http://127.0.0.1:5000/bookstatus/" + route.params.bookid + "?token=" + route.params.token, {
        method: "GET",
        headers: {
            "Content-type": "application/json",
        }
    })
        .then((response) => response.json())
        .then((data) => {
            alert(data.Alert)
            book.value = data.book
            mybook.value = data.mybook
            feedback.value = data.feedback
            console.log(book)
            console.log(mybook)
            console.log(admin)


        })
}
data()



</script>

<template>
    <main>
        <div style="display: flex; flex-direction: row;justify-content:space-between;">
            <img src="/src/assets/static/BL.png" width="65" height="65" style="margin:10px; margin-bottom: 5px;">
            
            <p class="title" style="font-size: 30px;padding-top: 10px;">
                <b>Book Status</b>
            </p>
            
            <img src="/src/assets/static/BL.png" width="65" height="65" style="margin:10px; margin-bottom: 5px;opacity: 0;">
        </div>
        <div align="center">
            <RouterLink :to="{ name: 'adminhome', params: { token: route.params.token } }" class="new">
                Home
            </RouterLink>
            <RouterLink :to="{ name: 'login' }" class="new">
                Log-Out
            </RouterLink>
        </div>

        <br>

        <div align="center">
            <table style="margin: auto;">

                <tr>
                    <td style="font-size: large;font-weight: bolder;color: aliceblue;">
                        <h2>{{ book.Name }} </h2>
                    </td>
                </tr>
                <tr>
                    <td style="color: gray;">
                        By {{ book.Author }}
                    </td>
                </tr>
                <br>
                <tr>
                    <td style="color: white;">
                        {{ book.Content }}
                    </td>
                </tr>
                <br>
                <br>
                <tr>
                    <h4 style="font-size: larger;">Feedbacks on {{ book.Name }}</h4>
                    <br>
                </tr>
                <tr v-for="feedbacks in feedback">
                    <td>
                        <br>
                        <p style="color: aliceblue;">User {{ feedbacks.UserId }}. {{ feedbacks.Feedback }}</p>
                        <br>
                    </td>
                </tr>
            </table>
            <br>
        </div>



    </main>
</template>../components/SectionCover.vue