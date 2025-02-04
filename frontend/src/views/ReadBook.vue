<script setup>

import { saveAs } from 'file-saver';
import { RouterLink } from 'vue-router';
import { useRoute } from 'vue-router'
import { onBeforeMount, onMounted, ref, watch } from 'vue'
import BookCover from '../components/BookCover.vue'


const route = useRoute()
const book = ref({})
const feedback_comment = ref("")


function data() {
    fetch("http://127.0.0.1:5000/readbook/" + route.params.bookid + "?token=" + route.params.token, {
        method: "GET",
        headers: {
            "Content-type": "application/json",
        }
    })
        .then((response) => response.json())
        .then((data) => {
            book.value = data.book
        })
}
data()

function export_book() {
    alert("Your Book will be downloaded in HTML format")

    fetch("http://127.0.0.1:5000/exportbook/" + route.params.bookid + "?token=" + route.params.token, {
        method: "GET",
        headers: {
            'Accept': 'application/json',
        },
    })
        .then(response => response.json())
        .then(json => {
            let inter = setInterval(() => {
                fetch("http://127.0.0.1:5000/taskstatus/" + json.tid + "?token=" + route.params.token, {
                    method: "GET",
                    headers: {
                        'Accept': 'application/json',
                    },
                })
                    .then(response => response.text())
                    .then(text => {
                        if (text === "True") {
                            window.location.assign("/src/assets/exports/" + book.value.Name + " by " + book.value.Author + ".html")
                            clearInterval(inter)
                        }
                    })

            }
                , 2000)
        })
}

const feedback = () => {
    const fd = new FormData()
    fd.append("feedback", feedback_comment.value)
    fetch("http://127.0.0.1:5000/feedback/" + route.params.bookid + "?token=" + route.params.token, {
        method: "POST",
        body: fd,
        headers: {
            'Accept': 'application/json',
        },
    })
        .then(response => response.json())
        .then(json => {
            if ('token' in json) {
                router.push({ name: "userhome", params: { token: json.token } })
            } else {
                alert(json.Alert)
            }
        });
}

</script>

<template>
    <main>
        <div style="display: flex; flex-direction: row;justify-content:space-between;">
            <img src="/src/assets/static/BL.png" width="65" height="65" style="margin:10px; margin-bottom: 5px;">

            <p class="title" style="font-size: 30px;padding-top: 10px;">
                <b>Read {{ book.Name }} by {{ book.Author }}</b>
            </p>
            <img src="/src/assets/static/BL.png" width="65" height="65"
                style="margin:10px; margin-bottom: 5px;opacity: 0;">
        </div>


        <div align="center">
            <RouterLink :to="{ name: 'userhome', params: { token: route.params.token } }" class="new">
                Home
            </RouterLink>
            <button @click="export_book" class="new">
                Export Book as HTML
            </button>
            <RouterLink :to="{ name: 'login' }" class="new">
                Log-Out
            </RouterLink>
        </div>

        <br>
        <br>

        <div align="center">
            {{ book.Content }}
        </div>

        <br>
        <br>
        <br>
        <br>
        <br>

        <div>

            <div align="center"
                style="border: 0.75px solid grey;border-radius:22px;width:222px;background:rgba(0,0,0,0.7);">
                <br>
                <label for='feedback'>Give Feedback</label>
                <br>
                <input v-model="feedback_comment" id='feedback_comment' type='text' name='feedback_comment' required>
                <br>
                <button @click="feedback" class="new" style="margin-bottom:10px;">
                    Post Feedback
                </button>
            </div>
        </div>
        <br>
        <br>

    </main>
</template>../components/SectionCover.vue