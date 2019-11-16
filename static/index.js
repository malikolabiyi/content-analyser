

const app = new Vue({
    el: '#app',
    data: {
        headline: '',
        focusKeyword: '',
        content: '',
        },
    methods: {
        clear: function() {
            this.headline = ''
            this.focusKeyword = ''
            this.content = ''
        }
    }
})
