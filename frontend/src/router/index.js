import {createRouter, createWebHistory, createWebHashHistory } from "vue-router"
import Login from '../views/Login.vue'
import CreateAcc from "../views/CreateAcc.vue"
import UserHome from "../views/UserHome.vue"
import AdminHome from "../views/AdminHome.vue"
import AdminBooks from "../views/AdminBooks.vue"
import EditSection from "../views/EditSection.vue"
import AddSection from "../views/AddSection.vue"
import AddBook from "../views/AddBook.vue"
import EditBook from "../views/EditBook.vue"
import BookStatus from "../views/BookStatus.vue"
import UserBooks from "../views/UserBooks.vue"
import MyBooks from "../views/MyBooks.vue"
import ReadBook from "../views/ReadBook.vue"
import UpdateAcc from "@/views/UpdateAcc.vue"

const router = createRouter({
    history: createWebHashHistory (import.meta.env.BASE_URL),
    routes: [
        {
            path:"/",
            name:"login",
            component: Login
        },
        {
            path:"/createaccount",
            name:'createaccount',
            component: CreateAcc
        },
        {
            path:"/userhome/:token",
            name:"userhome",
            component: UserHome,
            props : true
        },
        {
            path:"/adminhome/:token",
            name:"adminhome",
            component: AdminHome,
            props : true
        },
        {
            path:"/settings/:token",
            name:"settings",
            component:Login,
            props:true
        },
        {
            path:"/adminbooks/:token/:sectionid",
            name:"adminbooks",
            component:AdminBooks,
            props:true
        },
        {
            path:"/editsection/:token/:sectionid",
            name:"editsection",
            component:EditSection,
            props:true
        },
        {
            path:"/addsection/:token",
            name:"addsection",
            component:AddSection,
            props:true
        },
        {
            path:"/addbook/:token/:sectionid",
            name:"addbook",
            component:AddBook,
            props:true
        },
        {
            path:"/editbook/:token/:bookid",
            name:"editbook",
            component:EditBook,
            props:true
        },
        {
            path:"/bookstatus/:token/:bookid",
            name:"bookstatus",
            component:BookStatus,
            props:true
        },
        {
            path:"/userbooks/:token/:sectionid",
            name:"userbooks",
            component:UserBooks,
            props:true
        },
        {
            path:"/mybooks/:token",
            name:"mybooks",
            component:MyBooks,
            props:true
        },
        {
            path:"/readbook/:bookid/:token",
            name:"readbook",
            component:ReadBook,
            props:true
        },
        {
            path:"/accountupdate/:token",
            name:"updateaccount",
            component:UpdateAcc,
            props:true
        }


    ]
})

export default router