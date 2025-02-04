<script setup>
import { RouterLink } from 'vue-router'
import { useRoute } from 'vue-router'
import { ref, watch } from 'vue'


const route = useRoute()
let book = ref({})

function addBook() {

    if (!book.value.Name) {
        return alert("Book Name cannot be empty")
    }

    var jd = {
        "bookname": book.value.Name,
        "author": book.value.Author,
        "content": book.value.Content,
        "price": book.value.Price
    }

    fetch("http://127.0.0.1:5000/createbook/" + route.params.sectionid + "?token=" + route.params.token, {
        method: "POST",
        body: JSON.stringify(jd),
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then(response => response.json())
        .then(json => {
            alert(json.Alert)
        })
}

</script>

<template>
    <main>
        <div style="display: flex; flex-direction: row;justify-content:space-between;">
            <img src="/src/assets/static/BL.png" width="65" height="65" style="margin:10px; margin-bottom: 5px;">
            
            <h1 class="title" style="margin-top: 8px;font-size:35px">
                Add {{ book.Name }}
            </h1>
            
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
        <div align='center'>
            <div align='center' class="post-form">
                <br>

                <label for='name'>Book Name</label>
                <br>
                <input id='name' type='text' name="name" maxlength="25" v-model="book.Name" required>
                <br>

                <br>
                <label for='author'>Author</label>
                <br>
                <input id='author' type='text' name="description" maxlength="100" v-model="book.Author" required>
                <br>

                <br>
                <label for='content'>Content</label>
                <br>
                <input id='content' type='text' name="content" v-model="book.Content" required>
                <br>

                <br>
                <label for='price'>Price</label>
                <br>
                <input id='price' type='number' name="price" maxlength="10" v-model="book.Price" required>
                <br>

                <br>
            </div>
            <br>
            <br>
            <button @click="addBook" class="new" style="margin-bottom:10px;margin-top:10px;font-size: 20px;">
                Save Book
            </button>

        </div>
    </main>
</template>

<style scoped>
.chapter {
    border: 1px white solid;
    border-radius: 20px;
    margin: 15px;
    margin-top: 20px;
    padding: 20px;
    display: flex-box;
    width: fit-content;
    background: rgba(0, 0, 0, 0.5);
}

.post-form {
    display: inline-table;
    padding: 10px;
    border: 0.75px solid grey;
    border-radius: 22px;
    width: 222px;
    background: rgba(0, 0, 0, 0.7);
}

input[type='file'] {
    color: rgba(0, 0, 0, 0)
}
</style>