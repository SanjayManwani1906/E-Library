<script setup>
import { RouterLink } from 'vue-router'
import { useRouter, useRoute } from 'vue-router'
import { ref } from 'vue'


const router = useRouter()
const route = useRoute()
const username = ref("")
const email = ref("")

const updateaccount = () => {
    const fd = new FormData()
    fd.append("newname", username.value)
    fd.append("newemail", email.value)
    fetch("http://127.0.0.1:5000/updateaccount?token=" + route.params.token, {
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
                <b>Update Account</b>
            </p>
            
            <img src="/src/assets/static/BL.png" width="65" height="65" style="margin:10px; margin-bottom: 5px;opacity: 0;">
        </div>
        <div align="center">
            <RouterLink :to="{ name: 'userhome', params: { token: route.params.token } }" class="new">
                Home
            </RouterLink>
            <RouterLink :to="{ name: 'login' }" class="new">
                Log-Out
            </RouterLink>
        </div>
        <br>
        <div align='center'>
            <div align="center"
                style="border: 0.75px solid grey;border-radius:22px;width:222px;background:rgba(0,0,0,0.7);">
                <br>
                <label for='uname'>Username</label>
                <br>
                <input v-model="username" id='newname' type='text' name='newname' required>
                <br>
                <br>
                <label for='email'>Email Address</label>
                <br>
                <input v-model="email" id='newemail' type='text' name='newemail' required>
                <br>
                <br>
                <button @click="updateaccount" class="new" style="margin-bottom:10px;">
                    Update
                </button>
            </div>
        </div>
        <br>
        <br>
    </main>
</template>