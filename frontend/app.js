const API_URL="http://127.0.0.1:8000"

function showMessage(id,text,type){
    const msg=document.getElementById(id)
    msg.textContent=text
    msg.className=`message ${type}`
    msg.style.display="block"

    setTimeout(()=>{msg.style.display="none"},3000)
}

function getToken(){
    return localStorage.getItem("token")
}


async function register(){
    const username = document.getElementById("username").value
    const email = document.getElementById("email").value
    const password = document.getElementById("password").value

    if(!username || !email || !password){
        showMessage("message","Please fill in all fields", "error")
        return 
    }

    try{
        const response=await fetch(`${API_URL}/register`,{
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify({username,email,password})
        })

        const data=await response.json()

        if(response.ok){
            showMessage("message","Account created! Redirecting to login...","success")
            setTimeout(()=>{window.location.href="index.html"},2000)
        }else{
            showMessage("message",data.detail,"error")
        }
    }catch(error){
        showMessage("message","Server error. Try again.", "error")
    }
}



async function login() {
    const email = document.getElementById("email").value
    const password = document.getElementById("password").value

    if (!email || !password) {
        showMessage("message", "Please fill in all fields", "error")
        return
    }

    try {
        const response = await fetch(`${API_URL}/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        })

        const data = await response.json()

        if (response.ok) {
            localStorage.setItem("token", data.access_token)
            localStorage.setItem("username", email.split("@")[0])

            window.location.href = "dashboard.html"
        } else {
            showMessage("message", data.detail, "error")
        }

    } catch (error) {
        showMessage("message", "Server error. Try again.", "error")
    }
}



async function loadTasks() {
    const token = getToken()

    if (!token) {
        window.location.href = "index.html"
        return
    }

    const username = localStorage.getItem("username")
    document.getElementById("welcome-text").textContent = `Welcome, ${username}!`

    try {
        const response = await fetch(`${API_URL}/tasks?token=${token}`)
        const tasks = await response.json()

        if (response.ok) {
            displayTasks(tasks)
        } else {
            window.location.href = "index.html"
        }

    } catch (error) {
        console.error("Error loading tasks:", error)
    }
}



function displayTasks(tasks) {
    const taskList = document.getElementById("task-list")

    if (tasks.length === 0) {
        taskList.innerHTML = `
            <div class="empty-state">
                <p>No tasks yet. Create your first task!</p>
            </div>
        `
        return
    }

    taskList.innerHTML = tasks.map(task => `
        <div class="task-item ${task.completed ? 'completed' : ''}" id="task-${task.id}">
            <div class="task-left">
                <input 
                    type="checkbox" 
                    ${task.completed ? 'checked' : ''} 
                    onchange="toggleTask(${task.id}, this.checked)"
                >
                <div class="task-info">
                    <h4 class="${task.completed ? 'done' : ''}">${task.title}</h4>
                    <p>${task.description || ''}</p>
                </div>
            </div>
            <div class="task-actions">
                <button class="btn-danger" onclick="deleteTask(${task.id})">Delete</button>
            </div>
        </div>
    `).join("")
}



async function createTask() {
    const token = getToken()
    const title = document.getElementById("task-title").value
    const description = document.getElementById("task-description").value

    if (!title) {
        showMessage("message", "Task title is required", "error")
        return
    }

    try {
        const response = await fetch(`${API_URL}/tasks?token=${token}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title, description })
        })

        const data = await response.json()

        if (response.ok) {
            document.getElementById("task-title").value = ""
            document.getElementById("task-description").value = ""

            showMessage("message", "Task created!", "success")

            loadTasks()
        } else {
            showMessage("message", data.detail, "error")
        }

    } catch (error) {
        showMessage("message", "Server error. Try again.", "error")
    }
}



async function toggleTask(taskId, completed) {
    const token = getToken()

    try {
        await fetch(`${API_URL}/tasks/${taskId}?token=${token}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ completed })
        })

        loadTasks()

    } catch (error) {
        console.error("Error updating task:", error)
    }
}


async function deleteTask(taskId) {
    const token = getToken()

    try {
        await fetch(`${API_URL}/tasks/${taskId}?token=${token}`, {
            method: "DELETE"
        })

        loadTasks()

    } catch (error) {
        console.error("Error deleting task:", error)
    }
}

function logout() {
    localStorage.removeItem("token")
    localStorage.removeItem("username")
    window.location.href = "index.html"
}

if (window.location.pathname.includes("dashboard")) {
    loadTasks()
}