const level = document.querySelector("[level]")
const department = document.querySelector("[department]")
const course = document.querySelector("[course]")




level.addEventListener("change", async (e) =>{
        let defaultOption = document.createElement("option")
        defaultOption.innerText = "--Select Course--"
        course.innerHTML=""
        course.appendChild(defaultOption)
    // fetch all courses in the level 
    
    const response = await fetch(`/api/courses/${department.value}/${level.value}`)
    const data = await response.json()
    for (let d of data.data ) {
        let option = document.createElement("option")
        option.innerText = d.code +" - "+d.title
        option.value = d.code
        course.appendChild(option)
    }
})
