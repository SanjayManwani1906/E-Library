<script setup>

import { RouterLink } from 'vue-router';
import { useRoute } from 'vue-router'
import { onBeforeMount, onMounted, ref, watch } from 'vue'
import Cover from '../components/SectionCover.vue'


const route = useRoute()
const sections = ref([])
const user = ref([])
const search = ref("")
const search_sections = ref([])
const sections_dict = ref({})

function data() {
    fetch("http://127.0.0.1:5000/userhome?token=" + route.params.token, {
        method: "GET",
        headers: {
            "Content-type": "application/json",
        }
    })
        .then((response) => response.json())
        .then((data) => {
            user.value = data.user
            sections.value = data.sections
            sections_dict.value = data.sections_dict
        })
}

data()

function Search() {
    fetch("http://127.0.0.1:5000/search/sections/1/" + search.value + "?token=" + route.params.token, {
        method: "GET",
        headers: {
            "Content-type": "application/json",
        }
    })
        .then((response) => response.json())
        .then((data) => {
            search_sections.value = data.booklist
        })
}

watch(search, (curVal, oldVal) => {
    if (curVal === "") {
        search_sections.value = []
    } else {
        Search()
    }
})

</script>

<template>
    <main>
        <div style="display: flex; flex-direction: row;justify-content:space-between;">
            <img src="/src/assets/static/BL.png" width="65" height="65" style="margin:10px; margin-bottom: 5px;">

            <p class="title" style="font-size: 30px;padding-top: 10px;">
                <b>All Sections</b>
            </p>

            <img src="/src/assets/static/BL.png" width="65" height="65"
                style="margin:10px; margin-bottom: 5px;opacity: 0;">
        </div>
        <div style="display: flex; flex-direction: row;justify-content: center;">
            <RouterLink :to="{ name: 'mybooks', params: { token: route.params.token } }" class="new">
                My Books
            </RouterLink>
            <div class="form" style="padding-left:5px;padding-right:5px;margin-top: 10px;">
                <input v-model="search" id='search' placeholder="Search" type='search' name="search" style="border:0px;"
                    required>
            </div>
            <RouterLink :to="{ name: 'updateaccount', params: { token: route.params.token } }" class="new">
                Account Update
            </RouterLink>
            <RouterLink :to="{ name: 'login' }" class="new">
                Log-Out
            </RouterLink>
        </div>

        <br>

        <div align="center">
            <RouterLink v-if="search_sections.length == 0" v-for="section in sections"
                :to="{ name: 'userbooks', params: { token: route.params.token, sectionid: section.Id } }">
                <div class="post">
                    <table style="margin: auto;">

                        <tr>
                            <td style="font-size: large;font-weight: bolder;">
                                <h2>{{ section.Name }}</h2>
                            </td>
                        </tr>
                        <tr>
                            <td style="color: gray;">
                                {{ section.Description }}
                            </td>
                        </tr>
                    </table>
                </div>
            </RouterLink>

            <RouterLink v-if="search_sections.length != 0" v-for="section in search_sections"
                :to="{ name: 'userbooks', params: { token: route.params.token, sectionid: section.Id } }">
                <div class="post">
                    <table style="margin: auto;">

                        <tr>
                            <td style="font-size: large;font-weight: bolder;">
                                <h2>{{ section.Name }}</h2>
                            </td>
                        </tr>
                        <tr>
                            <td style="color: gray;">
                                {{ section.Description }}
                            </td>
                        </tr>
                    </table>
                </div>
            </RouterLink>

        </div>


    </main>
</template>../components/SectionCover.vue