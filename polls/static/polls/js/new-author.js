var form = new Vue({
    el: "#form",
    data: {
        countries: country.data,
        selectCountry: '中国',
        provinces: local,
        cities: [],
        areas: [],
        selectProvince: -1,
        selectCity: -1,
        selectArea: -1,
        afnamech: afnamech,
        alnamech: alnamech,
        afnameen: afnameen,
        alnameen: alnameen,
        amail: amail,
        cnamech1: cnamech1,
        cnamech2: cnamech2,
        cnameen1: cnameen1,
        cnameen2: cnameen2,
        czipcode: czipcode,
        addressch: addressch,
        addressen: addressen
    },
    watch: {
        selectProvince (i) {
            let province = local[i]
            console.log(i)
            this.cities = province.city
            this.selectCity = -1
        },
        selectCity (i) {
            if (i == -1) {
                this.areas = []
            } else {
                let city = local[this.selectProvince].city[i]
                this.areas = city.area
            }
            this.selectArea = -1
        }
    },
    methods: {
        checkForm (e) {
            if (this.selectCountry != '中国') {
                return true
            }

            if (this.selectProvince > -1 && this.selectCity > -1 && this.selectArea > -1) {
                return true
            }

            let errors = []

            if (this.selectProvince == -1) {
                errors.push('清选择省份')
            }

            if (this.selectCity == -1) {
                errors.push('请选择城市')
            }

            if (this.selectArea == -1) {
                errors.push('请选择区县')
            }

            alert(errors.join('\n'))
            e.preventDefault()
        }
    }
})