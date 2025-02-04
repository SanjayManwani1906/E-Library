<script setup>
import { RouterLink } from 'vue-router'
import { useRouter, useRoute } from 'vue-router'
import { ref } from 'vue'

const router = useRouter()

const username = ref("")
const password = ref("")

const login = () => {
  fetch("http://127.0.0.1:5000", {
    method: "POST",
    body: JSON.stringify({
      "username": username.value,
      "password": password.value,
    }),
    headers: {
      "Content-type": "application/json"
    }
  })
    .then(response => response.json())
    .then(json => {
      if ('token' in json) {
        if (json.authorisation == "user"){
          router.push({ name: "userhome", params: { token: json.token } })
        }else{
          router.push({name:"adminhome",params: {token: json.token}})
        }
        
      } else {
        alert(json.Alert)
      }
    });
}

</script>

<template>
  <main>
    <div align="center">
      <img src="/src/assets/static/BL.png" width="130" height="130" style="padding: 10px;margin-top: 10px;">
    </div>
    <div align="center">
      <RouterLink to="/createaccount" class="new" style="border:1px grey solid">
        Create New Account
      </RouterLink>
    </div>
    <br>
    <br>
    <div align="center">
      <div align="center" style="border: 0.75px solid grey;border-radius:22px;width:222px;background:rgba(0,0,0,0.7);">
        <br>
        <label for='uname'>Enter Username</label>
        <br>
        <input v-model="username" id='uname' type='text' name='uname'  required>
        <br>
        <br>
        <label for='uname'>Enter Password</label>
        <br>
        <input v-model="password" id='pass' type='password' name='pass' required>
        <br>
        <button @click="login" class="new" style="margin-bottom:10px;margin-top:10px;">
          Log In
        </button>
        <br>
      </div>
    </div>
  </main>
</template>