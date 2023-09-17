var pass = 0
var fail = 0
var total = 0
var chart = "";
var no_run = 0;
var total_tc_selected = 0

var iter=0;

$('#TC').on("click","button", function(){
    data=$(this).val();
    $.ajax({
            url:"/",
            type:"POST",
            data:{'data':data},
            
        });
});

$(document).ready(function () {
    $("#select_all").click(function () {
        // $(".testcases").attr('checked', this.checked);
        $(".testcases").prop('checked', $(this).prop('checked'));

    });
    
    $('.testcases').click(function(){
        $('#select_all').prop('checked', false);
    });
    $('.modules').click(function(){
        $('#select_module').prop('checked', false);
    });
});

$('#stop').click(function(){ 
    $('#clear_logs').prop('disabled', false);
    $('#stop').prop('disabled', true);
    $.ajax({  
        url:"/stop",  
        method:"POST",  
        data:{ "stop":"Stop"},  
        success:function(){  
            
        }  
    });  
});

$('#clear_logs').click(function(){
    location.reload();
});

$(document).ready(function() {
    var socket = io();

    socket.on('connect', function() {
        
        socket.emit('my_event', {data: 'I\'m connected!'});
    });

   
    socket.on('my_response', function(msg, cb) {
        var color = 'black';
        if (msg.data.includes('TestStep') == true  && msg.data.includes('Pass') == true){
            color="green"
        }
        else if(msg.data.includes('TestStep') == true  && msg.data.includes('FAIL') == true){
            color="red"
        }
        $('#log').append('<div style="color:'+color+'">' + $('<div/>').text( msg.data).html());
        if (cb)
            cb();
    });

    socket.on('charts_details', function(msg) {
        
        var pass_per = 0.0
        var fail_per = 0.0
        var no_run_per = 0.0

        // pass = pass + msg.pass_tc
        // fail = fail + msg.fail_tc
        total = msg.pass_tc + msg.fail_tc
        total_tc_selected=msg.total_count
        
        pass_per = (msg.pass_tc/total_tc_selected)*100
        fail_per = (msg.fail_tc/total_tc_selected)*100
        no_run = total_tc_selected - (total)
        no_run_per = (no_run/total_tc_selected)*100
        $('#total_tc_count').text(total_tc_selected);
        $('#total_pass_count').text(msg.pass_tc);
        $('#total_fail_count').text(msg.fail_tc);
        $('#no_run_count').text(no_run);
        $('#tc_count b').text("Total TC Selected: "+total_tc_selected);
        
        chart.series[0].setData([
            {name: pass +' PASS',y: pass_per,color:"#00FF00"}, 
            {name: fail +' FAIL',y: fail_per,color:"#FF0000"},
            {name: no_run +' No Run',y: no_run_per,color:"#2E2EFF"},
        ], true);

        // names=testcase_names.toString().split(',')[iter]
        // iter = iter + 1
        // data={'names':names,'r_id':msg.r_id,'pass':msg.pass_tc,'fail':msg.fail_tc}
        // $.ajax({  
        //     url:"/add_regression_logs",  
        //     method:"POST",  
        //     Accept : "application/json",
        //     contentType: "application/json",
        //     dataType: "json",
        //     data:JSON.stringify(data),  
        //     success:function(){  
        //         console.log('success=========')
        //     }  
        // }); 

        if (total == total_tc_selected){
            $('#stop').prop('disabled', true);
            $('#clear_logs').prop('disabled', false);
            iter = 0;
        }
        
    });
    
    socket.on('disconnect',()=>{
          socket.emit('client disconnected')
    });
});

// function show_charts(pass_per, fail_per, pass, fail){


chart = Highcharts.chart('container', {
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: '',
            // align: 'cenet'
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        accessibility: {
            point: {
                valueSuffix: '%'
            }
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: false
                },
                showInLegend: true
            }
        },
        series: [{
            // name: 'Brands',
            colorByPoint: true,
            data: [{
                name: '0 Pass',
                y: 0,
                color:"#00FF00"
            },  {
                name: '0 FAIL',
                y:0,
                color:'#FF0000'
            }, 
            {
                name: "No Run",
                y:100,
                color:'#2E2EFF'
            }, 
            
            ]
        }]
    });

$(function () {
    $('[data-toggle="tooltip"]').tooltip()
});

    
var checkboxes_value = []; 
var uncheckboxes_value = []; 
var module_id = "";
var module_id_arr = []; 
var testcase_names = [];

$("input:checkbox[name='modules[]']").click(function(){
    select_testcases()
});

$("#select_module").click(function () {
    $(".modules").prop('checked', $(this).prop('checked'));
    select_testcases()
});

  
function removeDuplicates(arr) {
    return arr.filter((item,
        index) => arr.indexOf(item) === index);
}


function select_testcases(){
    var modules = [];
    var check_module_id ="";   
    $("#tc_select").css('display','none');
    $("input:checkbox[name='modules[]']:checked").each(function(){    
        modules.push($(this).attr("id"));  
        check_module_id =   $(this).attr("id");		
    });
    
    

    
    $("input:checkbox[name='modules[]']:not(:checked)").each(function(){   
        unchecked_module = $(this).attr("id");
        uncheckboxes_value.push($(this).attr("id"));
        $("#show_"+unchecked_module).css('display','none');
        
    });

    for(let i=0.;i<modules.length;i++){
        module_id = modules[i].replace ( /[^\d.]/g, '' );
        module_id_arr.push(module_id)

        if ($("#module_"+module_id).is(":checked") == true){
            $("#show_module_"+module_id).css('display','block');
            $("#tc_select").css('display','block');
            uncheckboxes_value=removeDuplicates(uncheckboxes_value)
            remove_err_ele(uncheckboxes_value, modules[i])
            console.log("uncheckbox value===>",uncheckboxes_value)
        }
        
    }
    
}

$('#check_tc').click(function(){  
    checkboxes_value_1=[]
    for(let m=0;m<module_id_arr.length;m++){
        
        $("input:checkbox[name='testcase_module_"+module_id_arr[m]+"[]']").each(function(){  
                if(this.checked) {           
                    checkboxes_value_1.push($(this).val());                                                                               
                }  
            }); 
        }
      
        if(checkboxes_value_1.length == 0){
            alert("Please select atleast one TC..")
            var divelement = document.getElementById("exampleModal");
            divelement.style.display = 'none';
        }
});
function show_modal(div_id){
    // $('#exampleModal').css('display','block');
    var divelement = document.getElementById(div_id);
    divelement.style.display = 'block';
}
function close_window(div_id){
    var divelement = document.getElementById(div_id);
    divelement.style.display = 'none';
}
function run_tc(div_id){
    var text=$('#regression_name').val();
    var cmts_type=$("input[name=cmts_type]").val()
    if(text==""){
        alert('Please enter regression name...')
    }
    else{
        module_id_arr = removeDuplicates(module_id_arr)
        for(let k=0;k<uncheckboxes_value.length;k++){
            unchecked_module_id = uncheckboxes_value[k].replace ( /[^\d.]/g, '' );
            remove_err_ele(module_id_arr, unchecked_module_id)
        }
        for(let m=0;m<module_id_arr.length;m++){
        
        $("input:checkbox[name='testcase_module_"+module_id_arr[m]+"[]']").each(function(){  
                if(this.checked) {
                    testcase_names.push($(this).next('label').text());           
                    checkboxes_value.push($(this).val());                                                                               
                }  
            }); 
        }
        
        if(checkboxes_value.length == 0){
            alert("Please select atleast one TC..")
            var divelement = document.getElementById(div_id);
            divelement.style.display = 'none';
        }
        else{
            var divelement = document.getElementById(div_id);
            divelement.style.display = 'none';
            total_tc_selected = checkboxes_value.length;
            console.log("checkboxes_value===", checkboxes_value)
            checkboxes_value = checkboxes_value.toString(); 
            testcase_names=testcase_names.toString();
            $('#stop').prop('disabled', false);
            $('#check_tc').prop('disabled', true);
            $('#tc_count b').text("Total TC Selected: "+total_tc_selected);
            $('#total_tc_count').text(total_tc_selected);
            
            $.ajax({  
                url:"/logs",  
                method:"POST",  
                data:{ "data":checkboxes_value,'regression_name':text,'total_tc_selected':total_tc_selected,'cmts_type':cmts_type },  
                success:function(){  
                    
                }  
            }); 
           
            
        }   
    }
    
}

function remove_err_ele(array, val){
    const index = array.indexOf(val);
    if (index > -1){
        array.splice(index, 1)
    }
    console.log(array)
    return array;
}