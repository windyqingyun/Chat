function  startGetReplyTask(kfId) {
    //查看是否有回复
    setInterval(function () {

        $.ajax({
            url : '/getReply',
            data:{'id': kfId },
            cache : false,
            async : true,
            type : "POST",
            success : function (result){
                 //获取当前激活用户
                currentActive = $('.chat-user-list li.active').attr('id');

                if(result.message != '') {
                    chatRecord = result.message
                    if( currentActive ==  chatRecord.userId ){
                        $('.showContent').append('left:<h3>'+chatRecord.userName +':' + chatRecord.content + '</h3>')
                        $('.showContent').scrollTop( $('.msgContent')[0].scrollHeight);
                    }

                }

                if(result.users != null){

                    $('.chat-user-list').empty()

                    if(currentActive === undefined){
                       currentActive = result.users[0].id
                    }

                    for (var i = 0; i < result.users.length; i++) {
                        user = result.users[i]
                        _html = '<li id="' + user.id + '"> \
                                    <a href="#"> \
                                         <i class="fa fa-circle-o "></i> <span>' + user.name + '</span>\
                                    </a>\
                                 </li>';
                        $('.chat-user-list').append(_html)

                    }
                    $('#' + currentActive).addClass('active')

                    //重新绑定点击事件，不然失效
                    $('.chat-user-list li').on('click',function (){

                        $(this).addClass("active").siblings().removeClass("active");
                        $('#inputContent').val('')
                        $('.showContent').empty()
                        currentActive = $('.chat-user-list li.active').attr('id');

                         $.ajax({
                            url : '/getMsg',
                            data: {'kfId':kfId,'userId':currentActive},
                            cache : false,
                            async : true,
                            type : "POST",
                            success : function (result){
                                chatRecords = result.message
                                _html = ''
                                for(var i = 0 ; i < chatRecords.length ; i++){
                                    chatRecord = chatRecords[i]
                                    if( chatRecord.fromFlag == 'u' ){
                                        _html += 'u:<h3>'+chatRecord.userName +':' + chatRecord.content + '</h3>'
                                    }else{
                                        _html += 'k:<h3>'+chatRecord.kfName +':' + chatRecord.content + '</h3>'
                                    }
                                }
                                $('.showContent').append(_html)
                                $('.showContent').scrollTop( $('.showContent')[0].scrollHeight);

                            }
                        });

                    });


                }

            }
        });
     },5000);
}


function send(kfId,kfName) {
    var content = $('#inputContent').val()
    //正则替换
    content = content.replace(/\n/g,'<br/>')
    // userId = $('.chat-user-list li.active').attr('id')
    userId = 's'
    if (content == ''){
        alert('请输入内容')
    }
    else if (userId == undefined) {
        alert('请选择聊天对象')
    } else{
        $('.showContent').append('<h3>'+kfName+':'+content+'</h3>')

        userName = $('.chat-user-list li.active a span').text()

        data = {'content':content,'kfId':kfId,'kfName':kfName,'userId': userId,'userName':userName,'fromFlag':'k' }

        $.ajax({
            url : '/sendMsg',
            data: data,
            cache : false,
            async : true,
            type : "POST",
            success : function (result){
                $('#inputContent').val('')
                $('.showContent').scrollTop( $('.showContent')[0].scrollHeight);
            }
        });
    }
}
