
//REGISTRATION

function signUp(){
    var inputs = document.querySelectorAll('.input_form_sign');
    console.log(inputs);

    document.querySelectorAll('.ul_tabs > li')[0].className=""; // make SIGN IN unactive
    document.querySelectorAll('.ul_tabs > li')[1].className="active"; // make SIGN UP active

    for(var i = 0; i < inputs.length; i++) { //for each input
        if (inputs[i].classList.contains('sign-in-field')){
            inputs[i].className = "input_form_sign sign-in-field test";
        } else if(inputs[i].classList.contains('sign-up-field')){
            inputs[i].className = "input_form_sign sign-up-field d_block";
        }
    } // end for each input

    setTimeout( function(){
        $('.sign-up-field').each(function(){
            $(this).addClass('input_form_sign d_block active_inp');
        });
    },100 );

    document.querySelector('.link_forgot_pass').style.opacity = "0";
    document.querySelector('.link_forgot_pass').style.top = "-5px";

    document.querySelector('.btn-sign-in').style.display="none";
    document.querySelector('.btn-sign-up').style.display="block";

    setTimeout(function(){
        document.querySelector('.terms_and_cons').style.opacity = "1";
        document.querySelector('.terms_and_cons').style.top = "5px";
    },500);
    setTimeout(function(){
        document.querySelector('.link_forgot_pass').className = "link_forgot_pass d_none";
        document.querySelector('.terms_and_cons').className = "terms_and_cons d_block";
    },450);
} // end signUp()

function signUpFast(){
    var inputs = document.querySelectorAll('.input_form_sign');

    document.querySelectorAll('.ul_tabs > li')[0].className=""; // make SIGN IN unactive
    document.querySelectorAll('.ul_tabs > li')[1].className="active"; // make SIGN UP active

    for(var i = 0; i < inputs.length; i++) { //for each input
        if (inputs[i].classList.contains('sign-in-field')){
            inputs[i].className = "input_form_sign sign-in-field test";
        } else if(inputs[i].classList.contains('sign-up-field')){
            inputs[i].className = "input_form_sign sign-up-field d_block active_inp";
        }
    } // end for each input

    document.querySelector('.link_forgot_pass').style.opacity = "0";
    document.querySelector('.link_forgot_pass').style.top = "-5px";

    document.querySelector('.btn-sign-in').style.display="none";
    document.querySelector('.btn-sign-up').style.display="block";

    document.querySelector('.terms_and_cons').style.opacity = "1";
    document.querySelector('.terms_and_cons').style.top = "5px";
    document.querySelector('.link_forgot_pass').className = "link_forgot_pass d_none";
    document.querySelector('.terms_and_cons').className = "terms_and_cons d_block";
}

function signIn(){
    var inputs = document.querySelectorAll('.input_form_sign');
    document.querySelectorAll('.ul_tabs > li')[0].className = "active"; // make SIGN IN active
    document.querySelectorAll('.ul_tabs > li')[1].className = ""; // make SIGN UP unactive

    for(var i = 0; i < inputs.length ; i++  ) {
        if (inputs[i].classList.contains('sign-up-field')){
            inputs[i].className = "input_form_sign d_block sign-up-field";
            console.log('test1');
        }
    }

    setTimeout( function(){
        $('.sign-in-field').each(function(){
            $(this).addClass('input_form_sign d_block active_inp');
        });
    },100 );

    document.querySelector('.terms_and_cons').style.opacity = "0";
    document.querySelector('.terms_and_cons').style.top = "-5px";

    setTimeout(function(){
        document.querySelector('.terms_and_cons').className = "terms_and_cons d_none";
        document.querySelector('.link_forgot_pass').className = "link_forgot_pass d_block";
    },500);

    setTimeout(function(){
        document.querySelector('.link_forgot_pass').style.opacity = "1";
        document.querySelector('.link_forgot_pass').style.top = "5px";
    },1500);
    document.querySelector('.btn-sign-in').style.display="block";
    document.querySelector('.btn-sign-up').style.display="none";
} // end signIn()

function signInFast(){
    var inputs = document.querySelectorAll('.input_form_sign');
    document.querySelectorAll('.ul_tabs > li')[0].className = "active"; // make SIGN IN active
    document.querySelectorAll('.ul_tabs > li')[1].className = ""; // make SIGN UP unactive

    for(var i = 0; i < inputs.length ; i++  ) {
        if (inputs[i].classList.contains('sign-up-field')){
            inputs[i].className = "input_form_sign d_block sign-up-field";
        }
    }

    $('.sign-in-field').each(function(){
        $(this).addClass('input_form_sign d_block active_inp');
    });

    document.querySelector('.terms_and_cons').style.opacity = "0";
    document.querySelector('.terms_and_cons').style.top = "-5px";

    document.querySelector('.terms_and_cons').className = "terms_and_cons d_none";
    document.querySelector('.link_forgot_pass').className = "link_forgot_pass d_block";
    document.querySelector('.link_forgot_pass').style.opacity = "1";
    document.querySelector('.link_forgot_pass').style.top = "5px";

    document.querySelector('.btn-sign-in').style.display="block";
    document.querySelector('.btn-sign-up').style.display="none";
} // end signIn()

function showSnackbar() {
    var snackbar = $('#snackbar');
    snackbar.addClass('show');
    setTimeout(function(){ snackbar.removeClass('show'); }, 3000);
}

window.onload =function(){
    document.querySelector('.cont_centrar').className = "cont_centrar cent_active";
}

$(document).ready(function(){
    var html = $('#snackbar').html();
    var htmlToShow = "";
    html = html.replace(/\s/g,'');
    if (html != "")
        showSnackbar();
    /*
    $('#snackbar').bind("DOMSubtreeModified",function(){
        showSnackbar();
    });
    */
}); // end ready function

