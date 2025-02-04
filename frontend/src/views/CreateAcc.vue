<script setup>
import { RouterLink } from 'vue-router'
import { useRouter, useRoute } from 'vue-router'
import { ref } from 'vue'


const router = useRouter()

const username = ref("")
const password = ref("")
const cpassword = ref("")
const email = ref("")

const createaccount = () => {
    const fd = new FormData()
    fd.append("username", username.value)
    fd.append("password", password.value)
    fd.append("cpassword", cpassword.value)
    fd.append("email", email.value)
    fetch("http://127.0.0.1:5000/createaccount", {
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
        <br>
        <div align='center'>
            <h1 class='title'>
                Create Account
            </h1>
        </div>
        <br>
        <div align='center'>
            <div align="center"
                style="border: 0.75px solid grey;border-radius:22px;width:222px;background:rgba(0,0,0,0.7);">
                <br>
                <label for='uname'>Create Username</label>
                <br>
                <input v-model="username" id='uname' type='text' name='uname' required>
                <br>
                <br>
                <label for='email'>Email Address</label>
                <br>
                <input v-model="email" id='email' type='text' name='email' required>
                <br>
                <br>
                <label for='pass'>Create Password</label>
                <br>
                <input v-model="password" id='pass' type='text' name='pass' required>
                <br>
                <br>
                <label for='cpass'>Confirm Password</label>
                <br>
                <input v-model="cpassword" id='cpass' type='text' name='cpass' required>
                <br>
                <br>
                <button @click="createaccount" class="new" style="margin-bottom:10px;">
                    Create New Account
                </button>
            </div>
        </div>
        <br>
        <div align='center'>
            <RouterLink to="/" class='new' style="border:1px grey solid">
                Log in to existing account
            </RouterLink>
        </div>
        <br>
    </main>
</template>