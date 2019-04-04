var form2 = new Vue({
    el: "#form2",
    data: {
        showInfo: pifpub == 'true',
        ptype: "期刊[J]",
        pplace: pplace,
        ppub: ppub,
        pyear: pyear,
        ppage: ppage,
        ppath: ppath,
        pplaceError: false,
        ppubError: false,
        pyearError: false,
        ppageError: false,
        ppathError: false

    },
    computed : {
        showPath () {
            return this.ptype == "计算机程序[CP]" || this.ptype == "电子公告[EB]" || this.ptype == "数据库[DB]";
        }
    },
    methods: {
        beforeSubmit (event) {
            console.log(this.showInfo)
            if (this.showInfo === false) {
                return
            }

            this.pplaceError = false
            this.ppubError = false
            this.pyearError = false
            this.ppageError = false
            this.ppathError = false

            if (/^\s*$/.test(this.pplace)) {
                this.pplaceError = true
                console.log(1)
                event.preventDefault()
            }

            if (/^\s*$/.test(this.ppub)) {
                this.ppubError = true
                console.log(2)
                event.preventDefault()
            }

            if (this.pyear == "None" || /^\s*$/.test(this.pyear)) {
                this.pyearError = true
                console.log(3)
                event.preventDefault()
            }

            if (this.ppage == 'None' || /^\s*$/.test(this.ppage)) {
                this.ppageError = true
                console.log(4)
                event.preventDefault()
            }

            if (this.showPath && /^\s*$/.test(this.ppath)) {
                this.ppathError = true
                console.log(5)
                event.preventDefault()
            }
        }
    }
});