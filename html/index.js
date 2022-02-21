const app = {
    data() {
        return {
            cyclistWeightKg: 70.0,
            cyclistHeightCm: 181.4,
            cyclistFtpWKg: 5.15,
            cyclistMaxEnergyKj: 2088,

            profileIndex:0,

            courseLengthKm: 22.1,

            slopeData: "0,0;",
            headingData: "0,0;",
            windData: "0,0,0;",
            
            status:"",

            timeConsumptionS: 999999999,
            energyConsumptionKj: 999999999,

            imageWidthPercentage: 100,
            imageLeftPx: 10,
        }
    },

    watch: {
        courseLengthKm(newVal, oldVal) {
            chart.xAxis[0].update({
                max:newVal
            })

            chart.series[2].setData([[0, this.cyclistFtpWKg * this.cyclistWeightKg], [newVal, this.cyclistFtpWKg * this.cyclistWeightKg]])
        },
        cyclistFtpWKg(newVal, oldVal) {
            chart.series[2].setData([[0, newVal * this.cyclistWeightKg], [this.courseLengthKm, newVal * this.cyclistWeightKg]])
        },
        cyclistWeightKg(newVal, oldVal) {
            chart.series[2].setData([[0, this.cyclistFtpWKg * newVal], [this.courseLengthKm, this.cyclistFtpWKg * newVal]])
        },
        profileIndex(newVal, oldVal) {
            if (newVal < 0 || newVal > 3) {
                return
            }

            switch (newVal) {
                case 0:
                    this.cyclistWeightKg = 70.0
                    this.cyclistHeightCm = 181.4
                    this.cyclistFtpWKg = 5.15
                    this.cyclistMaxEnergyKj = 2088
                    break
                case 1:
                    this.cyclistWeightKg = 60.1
                    this.cyclistHeightCm = 170.0
                    this.cyclistFtpWKg = 4.70
                    this.cyclistMaxEnergyKj = 1000 // 1946.3
                    break
                case 2:
                    this.cyclistWeightKg = 71.5
                    this.cyclistHeightCm = 178.4
                    this.cyclistFtpWKg = 3.73
                    this.cyclistMaxEnergyKj = 2088
                    break
                case 3:
                    this.cyclistWeightKg = 59.8
                    this.cyclistHeightCm = 168.0
                    this.cyclistFtpWKg = 3.31
                    this.cyclistMaxEnergyKj = 935 // 1934.7
                    break
            }
        }
    },

    mounted() {
        window.submitCalculate=this.submitCalculate
    },

    updated() {
        chart.plotBGImage.attr({
            href: "./images/" + chartImageFile
        })
    },

    methods: {
        powerPlanColorChange(e) {
            chart.series[0].update({ color: e.target.value })
            chart.plotBGImage.attr({
                href: "./images/" + chartImageFile
            })
        },
        envelopeColorChange(e) {
            chart.series[1].update({ color: e.target.value })
            chart.plotBGImage.attr({
                href: "./images/" + chartImageFile
            })
        },
        btnApplyClick(e) {
            chart.series[0].setData(JSON.parse($("#in-power-plan").val().replace(",]", "]")))
            
            chart.plotBGImage.attr({
                href: "./images/" + chartImageFile
            })
        },
        btnClearClick(e) {
            chart.series[0].setData([[0, 0]])
            chart.series[1].setData([])
            $("#in-power-plan").val("[[0,0]]")

            chart.plotBGImage.attr({
                href: "./images/" + chartImageFile
            })

            console.log(chartImageFile)
        },
        submitCalculate() {
            if(chart.series[0].points.length==1){
                alert("ERROR: No positive POWER data")
                return
            }

            if (!checkDistances(chart.series[0].points, x => x.x)) {
                alert("ERROR: POWER data x series not beginning from 0 and strictly increasing")
                return
            }

            let pointsArrayStr = toPointsArrayString(chart.series[0].points)
            
            let slopeArrayStr = "["
            for (const i of this.slopeData.split(";")) {
                if (i.length > 0) {
                    let pair = i.split(",")
                    if (pair.length != 2) {
                        alert("ERROR: Invalid format in SLOPE data")
                        return
                    }
                    slopeArrayStr+=`[${pair[0]},${pair[1]}],`
                }
            }
            
            if (slopeArrayStr.length == 1) {
                alert("ERROR: No SLOPE data")
                return
            }

            slopeArrayStr += "]"

            slopeArrayStr = slopeArrayStr.replace(",]", "]")
            
            if (!checkDistances(JSON.parse(slopeArrayStr), x => x[0])) {
                alert("ERROR: SLOPE data distances not beginning from 0 and strictly increasing")
                return
            }
            
            let headingArrayStr = "["
            for (const i of this.headingData.split(";")) {
                if (i.length > 0) {
                    let pair = i.split(",")
                    if (pair.length != 2) {
                        alert("ERROR: Invalid format in HEADING data")
                        return
                    }
                    headingArrayStr += `[${pair[0]},${pair[1]}],`
                }
            }

            if (headingArrayStr.length == 1) {
                alert("ERROR: No HEADING data")
                return
            }

            headingArrayStr += "]"

            headingArrayStr = headingArrayStr.replace(",]", "]")

            if (!checkDistances(JSON.parse(headingArrayStr), x => x[0])) {
                alert("ERROR: HEADING data distances not beginning from 0 and strictly increasing")
                return
            }

            let windArrayStr = "["
            for (const i of this.windData.split(";")) {
                if (i.length > 0) {
                    let pair = i.split(",")
                    if (pair.length != 3||pair[1]<0||pair[1]>=360) {
                        alert("ERROR: Invalid format in WIND data")
                        return
                    }
                    windArrayStr += `[${pair[0]},${pair[1]},${pair[2]}],`
                }
            }

            if (windArrayStr.length == 1) {
                alert("ERROR: No WIND data")
                return
            }

            windArrayStr += "]"

            windArrayStr = windArrayStr.replace(",]", "]")

            if (!checkDistances(JSON.parse(windArrayStr), x => x[0])) {
                alert("ERROR: WIND data distances not beginning from 0 and strictly increasing")
                return
            }

            if (this.profileIndex < 0 || this.profileIndex > 3) {
                alert("ERROR: PROFILE INDEX out of range (0-3)")
                return
            }
            
            this.status="COMPUTING"

            axios.get("http://localhost:8897/", {
                params: {
                    cyclistWeightKg: this.cyclistWeightKg,

                    cyclistHeightM: this.cyclistHeightCm/100,
                    cyclistFtpWKg: this.cyclistFtpWKg,
                    cyclistMaxEnergyKj: this.cyclistMaxEnergyKj,

                    courseLengthKm: this.courseLengthKm,

                    profileIndex:this.profileIndex,

                    powerData: pointsArrayStr,
                    slopeData: slopeArrayStr,
                    headingData: headingArrayStr,
                    windData:windArrayStr
                }
            })
                .then(res => {
                    if (res.data.timeConsumptionS == Infinity
                        || res.data.timeConsumptionS == -Infinity
                        || isNaN(res.data.timeConsumptionS)) {
                        console.log(res)
                        //alert("ERROR: Response timeConsumptionS is (-)Infinity or NaN")
                        this.timeConsumptionS = 999999999
                        return
                    }

                    if (res.data.energyConsumptionKj == Infinity
                        || res.data.energyConsumptionKj == -Infinity
                        || isNaN(res.data.energyConsumptionKj)) {
                        console.log(res)
                        //alert("ERROR: Response energyConsumptionKj is (-)Infinity or NaN")
                        this.energyConsumptionKj = 999999999
                        return
                    }

                    this.timeConsumptionS = res.data.timeConsumptionS
                    this.energyConsumptionKj = res.data.energyConsumptionKj
                    chart.series[1].setData(res.data.plimData,true,false)
                    this.status=""
                })
                .catch(res => {
                    this.status="ERROR"
                    alert("Error requesting localhost at port: 8897")
            })
        }
    }
}

Vue.createApp(app).mount("#div-main-container")

function toPointsArrayString(chartPointsArray) {
    let pointsArrayStr = "["
    for (const i of chartPointsArray) {
        pointsArrayStr += `[${i.x},${i.y}],`
    }

    pointsArrayStr += "]"

    pointsArrayStr=pointsArrayStr.replace(",]","]")

    return pointsArrayStr
}

// check begins with zero and strictly increasing
function checkDistances(arr, getter) {
    if (arr.length > 0) {
        if (getter(arr[0]) != 0) {
            return false
        }
    }
    else {
        return false
    }

    for (let i = 1; i < arr.length; i++){
        if (getter(arr[i]) <= getter(arr[i - 1])) {
            return false
        }
    }

    return true
}

const chart = Highcharts.chart('div-power-plan', {
    chart: {
        events: {
            click: function (e) {
                // prevent accidentally adding a point directly above/below an existing point,
                // which causes "X SERIES NOT STRICTLY INCREASING" alert
                for(let i of this.series[0].points){
                    if (i.x == e.xAxis[0].value) {
                        return
                    }
                }

                this.series[0].addPoint([
                    e.xAxis[0].value,
                    e.yAxis[0].value
                ])

                $("#in-power-plan").val(toPointsArrayString(this.series[0].points))
                submitCalculate()
            }
        },
        plotBackgroundImage:"./images/course_profile_tokyo_men.jpg"
    },
    title: {
        text: ""
    },
    xAxis: {
        categories: [0],
        min: 0,
        max: 22.1,
        title: {
            text: "Distance/km"
        },
        gridLineWidth: 1,
        tickInterval: 1,
        tickWidth:1,
        minorTicks: true,
        minorTickWidth:1
    },
    yAxis: {
        min: 0,
        max: 2000,
        startOnTick: false,
        endOnTick: false,
        title: {
            text: "Power/W"
        }
    },
    tooltip: {
        enabled:false
    },
    // used as global series settings. can be overriden in series array
    plotOptions: {
        series: 
            {
                // force the x axis to start from extreme left
                pointPlacement: "on",
                tickmarkPlacement: "on"
            },
    },
    legend: {
        enabled: true,
        // layout: 'vertical',
        // align: 'right',
        verticalAlign: 'top'
    },
    series: [
        {
            name: "Power Plan",
            color: "#1591d1",
            data: [0],
            point: {
                events: {
                    click: function (e) {
                        if (this.series.data.length > 1 && this.series.data.indexOf(this) != 0) {
                            this.remove();
                            $("#in-power-plan").val(toPointsArrayString(chart.series[0].data))

                            if (chart.series[0].data.length == 1) {
                                chart.series[1].setData([])
                            }
                            else {
                                submitCalculate()
                            }

                            chart.plotBGImage.attr({
                                href: "./images/" + chartImageFile
                            })
                        }
                    }
                }
            }
        },
        {
            name: "Power Envelope",
            color: "#9d4b2a",
            data: [],
            enableMouseTracking: false,
            marker: {
                enabled: false
            },
            // prevent line from fading when hovered
            states: {
                inactive: {
                    opacity: 1
                }
            },
            lineWidth:1.5
        },
        {
            name: "FTP",
            color: "#ff0000",
            data: [[0, 70 * 5.15], [22.1, 70 * 5.15]],
            enableMouseTracking: false,
            marker: {
                enabled: false
            },
            states: {
                inactive: {
                    opacity: 1
                }
            }
        },
    ]
});

let chartImageFile ="course_profile_tokyo_men.jpg"
$("#in-image-file").change((e) => {
    if (e.target.files.length == 0) {
        return
    }

    chart.plotBGImage.attr({
        href: "./images/" + e.target.files[0].name
    })

    chartImageFile = e.target.files[0].name
})