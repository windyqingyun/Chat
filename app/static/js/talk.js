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
                        $('.showContent').scrollTop( $('.showContent')[0].scrollHeight);
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
                        UE.getEditor('editor').setContent('');
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
                                        _html += '<li>                                              \
                                                    <div class="leftSide" style="width: 45%;">    \
                                                        <div class="chat-info clearfix" style="width: auto;"> \
                                                            <span class="chat-name pull-left">'+chatRecord.userName+'</span>        \
                                                        </div>                                                      \
                                                        <div class="clearfix" style="width: 100%;">                \
                                                            <img class="chat-img" src="../static/img/favicon.ico" alt="">     \
                                                            <div style="width: 300px;float: left;">                     \
                                                                <div class="chat-text" style="width:auto;float: left;"> \
                                                                    '+chatRecord.content+'            \
                                                                </div>\
                                                            </div>\
                                                        </div>\
                                                    </div>\
                                                  </li>'
                                    }else{
                                        _html += '<li>                                              \
                                                    <div class="rightSide" style="width: 45%;">    \
                                                        <div class="chat-info clearfix" style="width: auto;"> \
                                                            <span class="chat-name pull-right">我</span>        \
                                                        </div>                                                      \
                                                        <div class="clearfix" style="width: 100%;">                \
                                                            <img class="chat-img" src="../static/img/favicon.ico" alt="">     \
                                                            <div style="width: 300px;float: right;">                     \
                                                                <div class="chat-text" style="width:auto;float: right;"> \
                                                                    '+chatRecord.content+'            \
                                                                </div>\
                                                            </div>\
                                                        </div>\
                                                    </div>\
                                                 </li>'
                                    }
                                }
                                $('.chat-msg').append(_html)
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
    var ue = UE.getEditor('editor')
    var content = ue.getContent();
    //正则替换
    // content = content.replace(/\n/g,'<br/>')
    // userId = $('.chat-user-list li.active').attr('id')
    userId = 's'
    if (content == ''){
        alert('请输入内容')
    }
    else if (userId == undefined) {
        alert('请选择聊天对象')
    } else{
        _html = '<li>                                              \
                    <div class="rightSide" style="width: 45%;">    \
                        <div class="chat-info clearfix" style="width: auto;"> \
                            <span class="chat-name pull-right">我</span>        \
                        </div>                                                      \
                        <div class="clearfix" style="width: 100%;">                \
                            <img class="chat-img" src="../static/img/favicon.ico" alt="">     \
                            <div style="width: 300px;float: right;">                     \
                            <div class="chat-text" style="width:auto;float: right;"> \
                                '+content+'            \
                            </div>\
                            </div>\
                        </div>\
                    </div>\
                </li>'
        $('.chat-msg').append(_html)

        userName = $('.chat-user-list li.active a span').text()

        data = {'content':content,'kfId':kfId,'kfName':kfName,'userId': userId,'userName':userName,'fromFlag':'k' }

        $.ajax({
            url : '/sendMsg',
            data: data,
            cache : false,
            async : true,
            type : "POST",
            success : function (result){
                ue.setContent('');
                ue.focus();
                $('.showContent').scrollTop( $('.showContent')[0].scrollHeight);
            }
        });
    }
}
