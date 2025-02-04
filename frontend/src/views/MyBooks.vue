<script setup>

import { RouterLink } from 'vue-router';
import { useRoute } from 'vue-router'
import { onBeforeMount, onMounted, ref, watch } from 'vue'
import BookCover from '../components/BookCover.vue'


const route = useRoute()
const user = ref('')
const my_books = ref([])

function data() {
    fetch("http://127.0.0.1:5000/mybooks?token=" + route.params.token, {
        method: "GET",
        headers: {
            "Content-type": "application/json",
        }
    })
        .then((response) => response.json())
        .then((data) => {
            user.value = data.user
            my_books.value = data.mybooks
        })
}
data()

console.log(my_books)


</script>

<template>
    <main>
        <div style="display: flex; flex-direction: row;justify-content:space-between;">
            <img src="/src/assets/static/BL.png" width="65" height="65" style="margin:10px; margin-bottom: 5px;">
            
            <p class="title" style="font-size: 30px;padding-top: 10px;">
                <b>My Books</b>
            </p>
            
            <img src="/src/assets/static/BL.png" width="65" height="65" style="margin:10px; margin-bottom: 5px;opacity: 0;">
        </div>

        <div align="center">
            <RouterLink :to="{ name: 'userhome', params: { token: route.params.token } }" class="new">
                Home
            </RouterLink>
            <RouterLink :to="{ name: 'login' }" class="new" >
                Log-Out
            </RouterLink>
        </div>

        <br>

        <div align="center">
            <RouterLink v-for="book in my_books"
                :to="{ name: 'readbook', params: { bookid: book.Id, token: route.params.token } }">
                <div class="post">
                    <table>
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
                    </table>
                </div>
            </RouterLink>
        </div>



    </main>
</template>../components/SectionCover.vue