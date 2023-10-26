const base = {
    get() {
        return {
            url : "http://localhost:8080/djangomg217/",
            name: "djangomg217",
            // 退出到首页链接
            indexUrl: 'http://localhost:8080/front/index.html'
        };
    },
    getProjectName(){
        return {
            projectName: "旅游景点推荐系统"
        } 
    }
}
export default base
