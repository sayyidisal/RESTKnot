function content_get(id){
   json_data = {
        "view": {
        "tags": {
            "id_record" : id
            }
        }
    }

    console.log(JSON.stringify(json_data))
    var content_data = ajaxDor("http://127.0.0.1:6968/api/content", json_data)
    content_data.done(function(respon){
        console.log(respon)
        // alert(respon.data)
    });

}

function addRecordNew(zone_id, record_name, type_name_id, ttl_id, json_content){
    var json_record_name = {
        "insert": {
           "fields": {
                "nm_record": record_name,
                "date_record":"2018070410",
                "id_type": type_name_id,
                "id_zone": zone_id
           }
        }
    }
    var save_onerecord= ajaxDor("http://127.0.0.1:6968/api/record",json_record_name)
    save_onerecord.done(function(respon){
        var id_record = respon.message['id']
        console.log("RECORD : ", respon)
        var json_ttl_data = {
                "insert": {
                    "fields": {
                        "id_record": respon.message['id'],
                        "id_ttl": ttl_id
                }
            }
        }

        var send_ttl = ajaxDor("http://127.0.0.1:6968/api/ttldata", json_ttl_data)
        send_ttl.done(function(respons){
            console.log("TTL DATA : ", respon)
            console.log("JSON _CONTENT",json_content)

            var p_array = json_content[0].serial_data.length - 1
            for(i=0; i< json_content.length;i++){
                var json_content_to = {
                    "insert": {
                       "fields": {
                           "id_ttldata": respons.message['id'],
                           "nm_content": json_content[i]['content_value']
                       }
                    }
                }
                if(json_content[i].serial_data == ""){
                    console.log("serial_data = ndak ada")
                    var reqs = ajaxDor("http://127.0.0.1:6968/api/content",json_content_to)
                    reqs.done(function(respon){
                        console.log("CONTENT : ", respon)
                        document.location.reload();
                    });
                }
                else{
                    var t_a = ""
                    var reqs = ajaxDor("http://127.0.0.1:6968/api/content",json_content_to)
                    reqs.done(function(respon){
                        console.log("CONTENT : ", respon)
                    });

                    for (a=0; a < json_content[i].serial_data.length;a++){
                        t_a += a
                        json_serial_data={
                            "insert": {
                               "fields": {
                                   "nm_content_serial": json_content[i].serial_data[a]['content_value_serial'],
                                   "id_record": id_record
                               }
                            }
                        }
                        var reqs = ajaxDor("http://127.0.0.1:6968/api/content_serial",json_serial_data)
                        reqs.done(function(respon){
                            console.log("SERIAL CONTENT : ", respon)
                        });
                    }
                    console.log("JUMLAY ARRAY",p_array)
                    if (t_a == p_array.toString()){
                        document.location.reload();
                    }
                }
            }
        });
    });
}

function ajaxDor(link,json_data){
    var req =  $.ajax({
        url:link,
        type:"POST",
        data: JSON.stringify(json_data),
        contentType:"application/json",
        dataType:"json"
    });
    return req
}

$(document).ready(function(){
    rule_content = [
        {
            "id" : "402329131320508417",
            "content": 1,
            "serial": 3,
            "name": "SRV"
        },
        {
            "name": "A",
            "content":1,
            "serial": 0,
            "id": "402386688803307521"
        },
        {
            "name": "CNAME",
            "content": 1,
            "serial":0,
            "id" : "402427533112147969"
        }
    ]

    $('#typename_id').change(function(){
        $("#serial_content_section").html("");
        $('#jns_record').val("")
        var typesid = $('#typename_id').val()
        for (a=0; a < rule_content.length; a++){
            if (typesid == rule_content[a].id){
                $('#jns_record').val(rule_content[a].name)
                for (i=1; i <= rule_content[a].content; i++){
                    var data = '<div class="form-group"><label>Serial Data</label><input type="text" class="form-control" id="content_name_'+i+'" /></div>'
                    $("#serial_content_section").append(data);
                    if(rule_content[a].serial > 0){
                        for(c=1; c <= rule_content[a].serial; c++){
                           var data_serial = '<div class="form-group"><label>Serial Data</label><input type="text" class="form-control" id="content_data_serial_'+c+'" /></div>'
                           $("#serial_data_content_section").append(data_serial);
                        }
                    }
                }
            }
        }
    });

    $('#btnAddRecord').click(function(){
        var record_spec = $('#jns_record').val()
        var json_content = []
        var record_name = $("#r_name").val()
        var ttl_id_name = $("#ttl_id_name").val()
        var zone_f_id = $("#zone_f_id").val()
        var type_name_id = $("#typename_id").val()
        for (a=0; a < rule_content.length; a++){
            if (record_spec == rule_content[a].name){
                var serial_data = []
                if(rule_content[a].serial > 0){
                    for(d=1; d <= rule_content[a].serial; d++){
                        var content_value_serial = $("#content_data_serial_"+d).val()
                        var json_content_data_serial = {
                            "content_value_serial": content_value_serial
                        }
                        serial_data.push(json_content_data_serial)
                    }
                }

                for(c=1; c <= rule_content[a].content; c++){
                    var content_value = $("#content_name_"+c).val()
                    console.log(rule_content[a].serial)
                    if(rule_content[a].serial > 0){
                        var json_content_data = {
                            "content_value": content_value,
                            "serial_data": serial_data
                        }
                        json_content.push(json_content_data)
                    }
                    else{
                        var json_content_data = {
                            "content_value": content_value,
                            "serial_data": ""
                        }
                        json_content.push(json_content_data)
                    }
                }
            }
        }
        addRecordNew(zone_f_id, record_name, type_name_id, ttl_id_name, json_content)
    });


     $('#btnCreateDomain').click(function(){
        $( "#form_domain" ).on( "submit", function(event) {
            var data = $(this).serializeArray();
            console.log(data)
            var request = $.post("http://127.0.0.1:6968/api/user/dnscreate", data);
            request.done(function(data){
                document.location.reload();
            });

            event.preventDefault();
        });
    });

    $('#record_section').hide();

    $.ajax({
        url: 'http://127.0.0.1:6968/api/zone',
        dataType: 'json',
        success: function(resp) {
            var table = $('#domain_table').DataTable({
                "select": true,
                "data": resp.data,
                "columns": [
                    { "data": "id_zone" },
                    { "data": "nm_zone" }
                ],
            });
            $('#domain_table tbody').on( 'click', 'tr', function (e) {
                $('#record_section').show()
                $('#record_table').html("")
                var data = table.row(this).data();
                
                json_data = {
                    "where": {
                       "tags": {
                           "id_zone": data.id_zone
                       }
                    }
                 }
                 $("#zone_f_id").val(data.id_zone)
                 $.ajax({
                    url:"http://127.0.0.1:6968/api/record",
                    type:"POST",
                    data: JSON.stringify(json_data),
                    contentType:"application/json",
                    dataType:"json",
                    
                    success: function(respon){
                        console.log(respon.data)
                        // $("record_table tbody").load(respon.data.data);
                        var $thead = $('<thead>').append(
                            $('<tr>').append(
                                $('<td>').text("Record ID"),
                                $('<td>').text("Record Name"),
                                $('<td>').text("Zone ID"),
                                $('<td>').text("Type Name ID"),
                                $('<td>').text("Content")
                            )
                        );
                        $('#record_table').append($thead)
                        tbody = $("<tbody>")
                        $.each(respon.data, function(i, item) {
                            var tr = $('<tr>').append(
                                $('<td>').text(item.id_record),
                                $('<td>').text(item.nm_record),
                                $('<td>').text(item.id_zone),
                                $('<td>').text(item.id_type),
                                $('<td>').html("<a href='#' onclick='content_get("+item.id_record+")' class='btn btn-xs content_btn'>Content</a>")
                            );
                            tbody.append(tr)
                        });
                        // console.log(tbody)
                        $('#record_table').append(tbody)

                        $.ajax({
                            url:"http://127.0.0.1:6968/api/type",
                            type:"GET",
                            success: function(respon){
                                var data = $.map(respon.data, function (obj) {
                                    obj.id = obj.id_type;
                                    obj.text = obj.nm_type; 
                                    return obj;
                                });
                                $('#typename_id').select2({
                                    data : data
                                });
                            }
                        });


                        $.ajax({
                            url:"http://127.0.0.1:6968/api/ttl",
                            type:"GET",
                            success: function(respon){
                                var data = $.map(respon.data, function (obj) {
                                    obj.id = obj.id_ttl;
                                    obj.text = obj.nm_ttl; 
                                    return obj;
                                });
                                $('#ttl_id_name').select2({
                                    data : data
                                });
                            }
                        });
                    }
                  });
            });
        }
    });
});