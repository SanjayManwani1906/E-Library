<script setup>

import { RouterLink } from 'vue-router';
import { useRoute } from 'vue-router'
import { onBeforeMount, onMounted, ref, watch } from 'vue'
import SectionCover from '../components/SectionCover.vue'


const route = useRoute()
const sections = ref([])
const user = ref([])
const admin = ref('admin')

function data() {
    fetch("http://127.0.0.1:5000/adminhome?token=" + route.params.token, {
        method: "GET",
        headers: {
            "Content-type": "application/json",
        }
    })
        .then((response) => response.json())
        .then((data) => {
            user.value = data.user
            sections.value = data.sections
        })
}
data()

function deleteSection(sid) {
    fetch("http://127.0.0.1:5000/deletesection/" + sid + "?token=" + route.params.token, {
        method: "GET",
        headers: {
            "Content-type": "application/json",
        }
    })
        .then((response) => response.json())
        .then((data) => {
            alert(data.Alert)
        })
    for (let section of sections.value) {
        if (section.Id == sid) {
            const i = sections.value.indexOf(section)
            sections.value.splice(i, 1)
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
            
            <img src="/src/assets/static/BL.png" width="65" height="65" style="margin:10px; margin-bottom: 5px;opacity: 0;">
        </div>
      
        <div align="center">
            <RouterLink class="new" :to="{ name: 'addsection', params: { token: route.params.token } }">
                    Add Section
            </RouterLink>
            <RouterLink :to="{ name: 'login' }" class="new">
                    Log-Out
                </RouterLink>
        </div>

        <br>

        <div align="center">
            <RouterLink v-for="section in sections"
                :to="{ name: 'adminbooks', params: { token: route.params.token, sectionid: section.Id } }">
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
                        <tr>
                            <td style="padding-top:0px;font-size:15px;">
                                <RouterLink class="new"
                                    :to="{ name: 'editsection', params: { token: route.params.token, sectionid: section.Id } }">

                                    Edit Section

                                </RouterLink>
                                <button @click.stop.prevent="deleteSection(section.Id)" class="new">
                                    Delete Section
                                </button>
                            </td>
                        </tr>
                    </table>
                </div>
            </RouterLink>

        </div>



    </main>
</template>../components/SectionCover.vue