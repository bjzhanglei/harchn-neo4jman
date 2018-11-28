/**
 * Created by harchn 2018.11
 */
function showinfo(sort, keys, info) {
    console.log(keys);
    console.log(info);
    var category = document.getElementById("sort_info");
    var info_div = document.createElement("div");
    var para = document.createElement("label");
    info_div.setAttribute("id", "tag");
    info_div.setAttribute("float", "left");
    para.setAttribute("id", "sort_color");
    console.log(sort);
    if (document.getElementById("tag")){
        category.removeChild(document.getElementById("tag"));
    }
    if (sort == "Sort") {
        para.setAttribute("style", "width: 40px;height: 20px;border-radius: 25px;float: left;text-align: center;" +
            "background-color: rgb(222, 155, 249); color: rgb(255, 255, 255)");
        para.innerHTML="Sort"
    } else if (sort == "Person") {
        para.setAttribute("style", "width: 62px;height: 20px;border-radius: 25px;float: left;text-align: center;" +
            "background-color: rgb(200,0,114); color: rgb(255, 255, 255)");
        para.innerHTML="Person"
    } else if (sort == "Movie") {
        para.setAttribute("style", "width: 62px;height: 20px;border-radius: 25px;float: left;text-align: center;" +
            "background-color: rgb(252,213,109); color: rgb(255, 255, 255)");
        para.innerHTML="Movie"
    } else if (sort == "Admin") {
        para.setAttribute("style", "width: 62px;height: 20px;border-radius: 25px;float: left;text-align: center;" +
            "background-color: rgb(228,161,225); color: rgb(255, 255, 255)");
        para.innerHTML="Admin"
    } else if (sort == "User") {
        para.setAttribute("style", "width: 62px;height: 20px;border-radius: 25px;float: left;text-align: center;" +
            "background-color: rgb(249,156,85); color: rgb(255, 255, 255)");
        para.innerHTML="User"
    }
    info_div.appendChild(para);
    for(var i = 0; i < keys.length; i++) {
        var info_label = document.createElement("label");
        info_label.setAttribute("style", "margin-left: 20px;");
        info_label.innerHTML=keys[i] + ": " + info[i];
        // console.log(info_label);
        info_div.appendChild(info_label);
    }
    category.appendChild(info_div);
}

Array.prototype.removeByValue = function() {
    var what, a = arguments, L = a.length, ax;
    while (L && this.length) {
        what = a[--L];
        while ((ax = this.indexOf(what)) !== -1) {
            this.splice(ax, 1);
        }
    }
    return this;
};