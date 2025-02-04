<script setup>

import { RouterLink } from 'vue-router';
import { useRoute } from 'vue-router'
import { onBeforeMount, onMounted, ref, watch } from 'vue'
import BookCover from '../components/BookCover.vue'


const route = useRoute()
const books = ref([])
const search_books = ref([])
const search = ref('')


function data() {
    fetch("http://127.0.0.1:5000/usergetbooks/" + route.params.sectionid + "?token=" + route.params.token, {
        method: "GET",
        headers: {
            "Content-type": "application/json",
        }
    })
        .then((response) => response.json())
        .then((data) => {
            books.value = data.books
        })
}
data()

function Search() {
    fetch("http://127.0.0.1:5000/search/books/" + route.params.sectionid + "/" + search.value + "?token=" + route.params.token, {
        method: "GET",
        headers: {
            "Content-type": "application/json",
        }
    })
        .then((response) => response.json())
        .then((data) => {
            search_books.value = data.booklist
        })
}

watch(search, (curVal, oldVal) => {
    if (curVal === "") {
        search_books.value = []
    } else {
        Search()
    }
})

function buybook(book_id) {
    fetch("http://127.0.0.1:5000/buybook/" + book_id + "?token=" + route.params.token, {
        method: "GET",
        headers: {
            "Content-type": "application/json",
        }
    })
        .then((response) => response.json())
        .then((data) => {
            alert(data.Alert)
        })
}

</script>

<template>
    <main>
        <div style="display: flex; flex-direction: row;justify-content:space-between;">
            <img src="/src/assets/static/BL.png" width="65" height="65" style="margin:10px; margin-bottom: 5px;">
            
            <p class="title" style="font-size: 30px;padding-top: 10px;">
                <b>All Books</b>
            </p>
            
            <img src="/src/assets/static/BL.png" width="65" height="65" style="margin:10px; margin-bottom: 5px;opacity: 0;">
        </div>
        <div style="display: flex; flex-direction: row;justify-content: center;">

            <RouterLink :to="{ name: 'userhome', params: { token: route.params.token } }" class="new">
                Home
            </RouterLink>
            <div class="form" style="padding-left:5px;padding-right:5px;margin-top: 10px;">
                <input v-model="search" id='search' placeholder="Search" type='search' name="search" style="border:0px;" required>
            </div>
            <RouterLink :to="{ name: 'login' }" class="new">
                    Log-Out
                </RouterLink>

        </div>


        <br>

        <div align="center" style="display: flex;flex-direction:row;justify-content: center;">
            <div v-if="search_books.length == 0" v-for="book in books" >
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
                        <tr>
                            <td>
                                <button @click.stop.prevent="buybook(book.Id)" class="new" style="color: white;">
                                    Buy Book for Rs.{{ book.Price }}
                                </button>
                            </td>
                        </tr>
                    </table>
                </div>

            </div>
            
            <RouterLink v-if="search_books.length != 0" v-for="book in search_books"
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
                        <tr>
                            <td>
                                <button @click.stop.prevent="buybook(book.Id)" class="new" style="color: white;">
                                    Buy Book
                                </button>
                            </td>
                        </tr>
                    </table>
                </div>

            </RouterLink>

        </div>



    </main>
</template>../components/SectionCover.vue