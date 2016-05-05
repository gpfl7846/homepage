var exist_check=false;
$(document).ready(function(){
	var running=1;
	
	$('input#email.form-control').keyup(function(){
		if (running==1){
			var text=$(this).val();
		if (text!=""){
			$.ajax({
				url: '/find_user',
				type: 'POST',
				data: {'text':text},
				success:function(response){					
					if (response=="user exist"){
						console.log('user exist');
						//$('#message_email').empty()
						//$('#message_email').append(response)
						running=1;
						alert('중복된 아이디 입니다. 아이디를 변경해주세요.');
						exist_check=true;
					}
					else{
						console.log('user not exist');
						running=1;
						exist_check=false;
					}
				},
				error:function(){
					//console.log(text)
					//console.log('error');
				},
				complete:function(){
					//console.log('complete!');
				}
			});
		} 
	
		else {
			//console.log('this is blank');
			//$('#message_email').empty()
			//exist_check=false;
		}
	}
	});

	//
// 	$("input.pull-right.team_name.form-control.password").keyup(function(){
// 		if (running==1){
// 			var password=$("input.pull-right.team_name.form-control.password").val();
// 		if (password!=""){
// 			$.ajax({
// 				url: '/check_password',
// 				type: 'POST',
// 				data: {'password':password},
// 				success:function(response){
					
// 					if (response!=0){
// 						$('#message_password').empty()
// 						$('#message_password').append(response)
// 						running=1;
// 					}
// 					else{
// 						running=0;
// 					}
// 				},
// 				error:function(){
// 					//console.log(password)
// 					//console.log('error')
// 				},
// 				complete:function(){
// 					//console.log('complete!');
// 				}
// 			});
// 		} 
	
// 		else {
// 			$('#message_password').empty()
// 		}
// 	}
// 	});
// 	//
// 	$("input.pull-right.team_name.form-control.password_check").keyup(function(){
// 		if (running==1){
// 			var password_check=$("input.pull-right.team_name.form-control.password_check").val();
// 		if (password_check!=""){
// 			$.ajax({
// 				url: '/check_password_check',
// 				type: 'POST',
// 				data: {'password_check':password_check,
// 				'password':$("input.pull-right.team_name.form-control.password").val()},
// 				success:function(response){
					
// 					if (response!=0){
// 						$('#message_password_check').empty()
// 						$('#message_password_check').append(response)
// 						running=1;
// 					}
// 					else{
// 						running=0;
// 					}
// 				},
// 				error:function(){
// 					//console.log(password_check)
// 					//console.log('error')
// 				},
// 				complete:function(){
// 					//console.log('complete!');
// 				}
// 			});
// 		} 
	
// 		else {
// 			$('#message_password_check').empty()
// 		}
// 	}
// 	});

	

});

//
	function testAlertBox() {
			//(document.getElementById("profile_img").value !="")&&
	  		if((exist_check==false)&&(document.joinForm.username.value!="")&&(document.joinForm.birthday.value!="")&&(document.joinForm.college.value!="")&&(document.joinForm.major.value!="")&&(document.joinForm.student_id.value!="")&&(document.joinForm.phone.value!="")&&(document.joinForm.email.value!="")&&(document.joinForm.password.value!="")&&(document.joinForm.password_check.value!="")&&(document.joinForm.password.value==document.joinForm.password_check.value)&&(document.joinForm.agree.checked==true)){
	  			document.joinForm.submit();
	  			return true;
	  			}
	  		else if (document.joinForm.username.value==""){
		    	alert('이름을 입력해 주세요.');
		    	document.joinForm.username.focus();
		    	return false;
		    }
		    else if (document.joinForm.birthday.value==""){
		    	alert('생년월일을 입력해 주세요.(예-901212)');
		    	document.joinForm.birthday.focus();
		    	return false;
		    }
		    else if (document.joinForm.college.value==""){
		    	alert('어느단과대 소속이신가요?');
		    	document.joinForm.college.focus();
		    	return false;
		    }
		    else if (document.joinForm.major.value==""){
		    	alert('전공을 입력해 주세요.');
		    	document.joinForm.major.focus();
		    	return false;
		    }
		    else if (document.joinForm.student_id.value==""){
		    	alert('학번을 입력해주세요.');
		    	document.joinForm.student_id.focus();
		    	return false;
		    }
		    else if (document.joinForm.phone.value==""){
		    	alert('전화번호를 입력해주세요.(예 : 010-1234-5678)');
		    	document.joinForm.phone.focus();
		    	return false;
		    }
		    else if (document.joinForm.email.value==""){
		    	alert('email을 입력해주세요');
		    	document.joinForm.email.focus();
		    	return false;
		    }
		    else if (document.joinForm.password.value==""){
		    	alert('비밀번호를 입력해주세요.');
		    	document.joinForm.password.focus();
		    	return false;
		    }
		    else if (document.joinForm.password_check.value==""){
		    	alert('비밀번호를 한 번 더 입력하세요.');
		    	document.joinForm.password_check.focus();
		    	return false;
		    }
		    else if(document.joinForm.password.value!=document.joinForm.password_check.value){
		    	alert('비밀번호와 비밀번호 확인이 같지 않습니다!');
		    	return false;
		    }
		    // else if (document.getElementById("profile_img").value == ""){
		    // 	alert('선수프로필을 위해 사진을 등록해주세요.');
		    // 	return false;
		    // }
		    else if (document.joinForm.agree.checked!=true){
		    	alert('이용약관에 동의하셔야 합니다.');
		    	return false;
		    }
		    else if (exist_check==true){
		    	alert('중복되지 않는 이메일을 사용하십시오.');
		    	return false;
		    }		
		}
