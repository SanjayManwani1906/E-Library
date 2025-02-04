<script setup>

import { RouterLink } from 'vue-router';
import { useRoute } from 'vue-router'
import { onBeforeMount, onMounted, ref, watch } from 'vue'
import BookCover from '../components/BookCover.vue'


const route = useRoute()
const books = ref([])
const admin = ref('admin')


function data() {
    fetch("http://127.0.0.1:5000/getbooks/" + route.params.sectionid + "?token=" + route.params.token, {
        method: "GET",
        headers: {
            "Content-type": "application/json",
        }
    })
        .then((response) => response.json())
        .then((data) => {
            books.value = data.books
            console.log(books.value)
        })
}
data()

function deleteBook(bid) {
    fetch("http://127.0.0.1:5000/deletebook/" + bid + "?token=" + route.params.token, {
        method: "GET",
        headers: {
            "Content-type": "application/json",
        }
    })
        .then((response) => response.json())
        .then((data) => {
            alert(data.Alert)
        })
    for (let book of books.value) {
        if (book.Id == bid) {
            const i = books.value.indexOf(book)
            books.value.splice(i, 1)
        }
    }
}


</script>

<template>
    <main>
        <div style="display: flex; flex-direction: row;justify-content:space-between;">
            <img src="/src/assets/static/BL.png" width="65" height="65" style="margin:10px; margin-bottom: 5px;">

            <p class="title" style="font-size: 30px;padding-top: 10px;">
                <b>All Books</b>
            </p>

            <img src="/src/assets/static/BL.png" width="65" height="65"
                style="margin:10px; margin-bottom: 5px;opacity: 0;">
        </div>
        <div align="center">
            <RouterLink :to="{ name: 'adminhome', params: { token: route.params.token } }" class="new">
                Home
            </RouterLink>
            <RouterLink
                :to="{ name: 'addbook', params: { sectionid: route.params.sectionid, token: route.params.token } }"
                class="new">
                Add Book
            </RouterLink>
            <RouterLink :to="{ name: 'login' }" class="new">
                Log-Out
            </RouterLink>
        </div>

        <br>

        <div align="center">
            <RouterLink v-for="book in books"
                :to="{ name: 'bookstatus', params: { token: route.params.token, bookid: book.Id } }">
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
                        <tr v-if="authorisation = 'admin'">
                            <td style="padding-top:0px;font-size:15px;">
                                <RouterLink class="new"
                                    :to="{ name: 'editbook', params: { token: route.params.token, bookid: book.Id } }">
                                    Edit Book
                                </RouterLink>
                                <button @click.stop.prevent="deleteBook(book.Id)" class="new">
                                    Delete Book
                                </button>
                            </td>
                        </tr>
                    </table>
                </div>

            </RouterLink>

        </div>



    </main>
</template>../components/SectionCover.vue