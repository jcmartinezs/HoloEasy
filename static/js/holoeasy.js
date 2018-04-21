"use strict";

function HoloEasy(){

	var self = this;
    //$(":file").filestyle();
    self.obj = objeto.beamShaping;
    self.imagenes = objeto.imagenes;
    self.contador = 0;    
    self.fileName = "";
    self.contenType = "";
    
    self.seleccionarImagen = function(imagen){
        if(imagen == 'file'){
            $timeout(function(){$( "#OBJ" ).click();},500)
        }   
    };
    self.imagenAReconstruir = function(){
        signal_a_reconstruire(getFormulario());
    }
    self.empezar = function(){
        self.obj.niveaux = $("#niveaux").val();
        self.obj.analogo_PRs = $("#analogo_PRs").val();
        self.obj.analogo_PRb = $("#analogo_PRb").val();
        self.obj.analogo_DPRA = $("#analogo_DPRA").val();
        self.obj.analogo_DPLRA = $("#analogo_DPLRA").val();
        self.obj.analogo_iteraccion = $("#iteranalogo").val();
        self.obj.cuantificar_PRs = $("#cuantificar_PRs").val();
        self.obj.cuantificar_PRb = $("#cuantificar_PRb").val();
        self.obj.cuantificar_DPRA = $("#cuantificar_DPRA").val();
        self.obj.cuantificar_DPLRA = $("#cuantificar_DPLRA").val();
        self.obj.cuantificar_iteraccion = $("#iterquantization").val();

        self.obj.taillesignal = $("#taillesignal").val();
        self.obj.tailleholo = $("#tailleholo").val();
        $("#portfolio-cuantificado").css("display","none");
        calcular_holograma();
    };
    self.descargarImagen = function(){
        if(self.obj.niveaux<255 && self.obj.cuantificar=='SI'){//Cuantificado
            descargarCuantizado('holo.png',self.obj.holoef);
        }else{//Analogico
            descargarAnalogico('holo.png',self.obj.U_Gj);
        }
    };
    
    self.descargarHolograma = function(imagen,tipo){
        console.log(tipo);
        console.log(imagen);
        var data = { imagen:imagen, tipo:tipo, datos: (tipo=='C' ? self.obj.holoef : self.obj.U_Gj) };
        $.ajax({
            type:"POST",
            url: '/downloadFile',
            data: JSON.stringify(data),
            contentType: "application/json; charset=utf-8",
            responseType:'arraybuffer',
            processData: false,
            success: downloadFile,
            error: errorDownloadFile
        });
    };

    inicializar();
    function inicializar(){
        $("#archivo").change(function(){
        	self.contador++;
        	addImage(this);
        });
        $("#pixelmargin").val(self.obj.pixelmargin);
        $("#niveaux").val(self.obj.niveaux);
        $("#analogo_PRs").val(self.obj.PRs);
        $("#analogo_PRb").val(self.obj.PRb);
        $("#analogo_DPRA").val(self.obj.DPRA);
        $("#analogo_DPLRA").val(self.obj.DPLRA);
        $("#cuantificar_PRs").val(self.obj.PRs);
        $("#cuantificar_PRb").val(self.obj.PRb);
        $("#cuantificar_DPRA").val(self.obj.DPRA);
        $("#cuantificar_DPLRA").val(self.obj.DPLRA);
        $("#iteranalogo").val(self.obj.iterquantization);
        $("#iterquantization").val(self.obj.iterquantization);
        self.saveData = (function () {
            var a = document.createElement("a");
            document.body.appendChild(a);
            a.style = "display: none";
            return function (data, fileName) {
                var url = window.URL.createObjectURL(data);
                a.href = url;
                a.download = fileName;
                a.click();
                window.URL.revokeObjectURL(url);
            };
        }());
    };

    function addImage(input) {
        self.obj.tipoimg = 'file';
        self.imagenAReconstruir();
        //imageType = /image.*/;
        /*if (!file.type.match(imageType))
            return;
        var reader = new FileReader();
        reader.onload = fileOnload;
        reader.readAsDataURL(file);*/
    };
    //Esta funcion se enecarga de colocar la imagen en la pagina.
    function fileOnload(e) {
        var result=e.target.result;
        $('#imagen').attr("src",result);
    }
    
    function getFormulario (){
        var formData = new FormData();
        formData.append("tipoimg", 'file');
        formData.append("cuantificar", self.obj.cuantificar);
        formData.append("tailleimg",$("#tailleimg").val());
        formData.append("pixelmargin",self.obj.pixelmargin);
        formData.append("OBJ",$("#archivo").get(0).files[0]);
        formData.append("fase",self.obj.phase);
        formData.append("fase_inicial",self.obj.phaseinitial);
        formData.append("iteraccion",self.obj.iterquantization);
        formData.append("control_banda",self.obj.controlbande);
        formData.append("diffphase",self.obj.diffphase);
        formData.append("PRs",self.obj.PRs);
        formData.append("PRb",self.obj.PRb);
        formData.append("DPRA",self.obj.DPRA);
        formData.append("DPLRA",self.obj.DPLRA);
        formData.append("DPE",self.obj.DPE);
        formData.append("nivel",self.obj.niveaux);
        formData.append("MASIRdes",self.obj.MASIRdes);
        formData.append("tipoilum",self.obj.tipoilum);
        formData.append("taillesignal",self.obj.taillesignal);
        formData.append("tailleholo",self.obj.tailleholo);
        formData.append("iterODD",self.obj.iterODD);
        return formData;
    };

    function modalEsperaTitulo(titulo){
        $("#titulo-estado").html(titulo);
    };

    function modalEspera(titulo){
        $("#titulo-estado").html(titulo);
        $("#modalEspera").modal("show");
    };

    function ocultarModal(){
        $("#modalEspera").modal("hide");
    };

    function signal_a_reconstruire(obj){
        modalEspera("Señal a reconstruir...");
        $.ajax({
            type:"POST",
            url: '/signal_a_reconstruire',
            data: obj,
            dataType: 'json',
            processData: false, 
            contentType: false,
            success: function(data){
                console.log(data);
                ocultarModal();
                self.imagenes.imagen1 = data.imagen;
                $('#imagen').attr("src",self.imagenes.imagen1);
                self.obj.id_proceso = data.id_proceso;
                self.obj.tailleobject = data.Nobj;
                self.obj.tailleimg =  data.Nobj;
                $("#tailleimg").val(self.obj.tailleobject);
                $("#tailleholo").val(self.obj.tailleobject);
                $("#taillesignal").val(self.obj.tailleobject*2);
            },
            error: function(error){
                $("#archivo").val("");
                errorPeticion(error);
            }
        });
    };
    self.aplicacionOptica = function(valor){
        aplicacionOptica(valor.checked);
    };
    self.cuantificarHolograma = function(valor){
        cuantificarHolograma(valor.checked);
    };
    function calcular_holograma(){
        $("#dos_a").addClass("corazon");
        self.obj.tailleobject = $("#tailleobject").val();
        self.obj.iterODD = $("#iterquantization").val();
        self.obj.Nobj = $("#tailleimg").val();
        self.obj.code = 'codedur';//codedoux,codedur
        self.obj.MASIRdes = 0.8;
        self.obj.controlbande = 0.01;
        self.obj.diffphase = 1.335;
        self.obj.nivel = $("#niveaux").val();
        self.obj.PRs = $("#PRs").val();
        self.obj.PRb = $("#PRb").val();
        self.obj.DPRA = $("#DPRA").val();
        self.obj.DPLRA = $("#DPLRA").val();
        self.obj.DPE = 0;
        self.obj.iteraccion = $("#iterquantization").val();
        phase_initial();  
    };
    function phase_initial(){
        modalEspera("Fase Inicial...");
        console.log(self.obj);
        $.ajax({
            type:"POST",
            url: '/phase_initial',
            data: JSON.stringify(self.obj),
            contentType: "application/json; charset=utf-8",
            dataType: 'json',
            success: function(data){
                console.log(data);
                diffuseur_calculer(); 
            },
            error: errorPeticion
        });
    };
    function diffuseur_calculer(obj){
        modalEsperaTitulo("Cálculo del difusor...");
        $.ajax({
            type:"POST",
            url: '/calculer_diffuseur',
            data: JSON.stringify(self.obj),
            contentType: "application/json; charset=utf-8",
            dataType: 'json',
            success: function(data){
                self.imagenes.imagen2 = data.imagen2;
                self.imagenes.imagen3 = data.imagen3;
                self.obj.masirREF = data.masirREF;

                self.obj.s1 = data.s1==undefined?0:data.s1;
                self.obj.s2 = data.s2==undefined?0:data.s2;
                
                self.obj.masiroid = data.masiroid;
                self.obj.ffsin = data.ffsin;
                self.obj.TFOID = data.TFOID;
                self.obj.ODD = data.ODD;
                self.obj.OID = data.OID;
                diffuseur_optimiser(obj); 
            },
            error: errorPeticion
        });
    };
    function diffuseur_optimiser(obj){
        modalEsperaTitulo("Cálculo del difusor . . . ");
        $.ajax({
            type:"POST",
            url: '/calculer_diffuseur/optimiser',
            data: JSON.stringify(self.obj),
            contentType: "application/json; charset=utf-8",
            dataType: 'json',
            success: function(data){
                if(self.obj.phase == 'phasealea' && self.obj.phaseinitial == 'pasbandelimite'){
                    
                }else{
                    self.imagenes.imagen2 = data.imagen2;
                    self.imagenes.imagen3 = data.imagen3;
                    $('#imagen2').attr("src",self.imagenes.imagen2);
                    $('#imagen3').attr("src",self.imagenes.imagen3);
                    self.obj.DSdiff = data.DSdiff;
                    self.obj.masirODD = data.masirODD;
                    self.obj.ODD = data.ODD;
                    self.obj.FD = data.FD;
                }
                //Next
                analogiqueIlumination();
            },
            error: errorPeticion
        });
    }
    // 4
    function analogiqueIlumination(obj){
        modalEsperaTitulo("Cálculo del holograma...");
        $.ajax({
            type:"POST",
            url: '/hologramme_analogique/ilumination',
            data: JSON.stringify(self.obj),
            contentType: "application/json; charset=utf-8",
            dataType: 'json',
            success: function(data){
                voir();
            },
            error: function(data){
                alert("Ocurrió un error al procesar la solicitud, inténtelo más tarde");
                console.log(data)
            }
        });
    }
    function voir (){
        modalEsperaTitulo("Cálculo del holograma . . .");
        $.ajax({
            type:"POST",
            url: '/hologramme_analogique/voir',
            data: JSON.stringify(self.obj),
            contentType: "application/json; charset=utf-8",
            dataType: 'json',
            success: function(data){
                //$('#imagen4').attr("src",self.imagenes.imagen4);
                //$('#imagen5').attr("src",self.imagenes.imagen5);
                analogiqueOptimiser();
            },
            error: errorPeticion
        });
    }
    function analogiqueOptimiser(){
        modalEsperaTitulo("Cálculo del holograma...");
        $.ajax({
            type:"POST",
            url: '/hologramme_analogique/optimiser',
            data: JSON.stringify(self.obj),
            contentType: "application/json; charset=utf-8",
            dataType: 'json',
            success: function(data){

                //$("#imagen-holo").attr("src",data.imagen4);
                //$("#imagen-holo-1").attr("src",data.imagen4);
                analogiqueCalculer();
            },
            error: errorPeticion
        });
    }
    function analogiqueCalculer (){
        modalEsperaTitulo("Cálculo del holograma . . .");
        $.ajax({
            type:"POST",
            url: '/hologramme_analogique/calculer',
            data: JSON.stringify(self.obj),
            contentType: "application/json; charset=utf-8",
            dataType: 'json',
            success: function(data){
                $("#reconstruccion-analogica").attr("src",data.reconstruccion);
                $("#holograma-analogico").attr("src",data.holograma);
                $("#analogico-eqm").html(data.analogicoEqm);
                $("#analogico-ed").html(data.analogicoEd);
                $("#analogico-rsb").html(data.analogicoRsb);
                $("#analogico-u").html(data.analogicoU);
                $("#analogico-zb").html(data.analogicoZb);
                $("#analogico-ds").html(data.analogicoDs);
                enlacesDescargarReconstruir("#descargar-reconstruccion-analogica",data.enlaceReconstruir);
                enlacesDescargarHolo("#descargar-holograma-analogico",data.enlaceHolograma);
                if(self.obj.niveaux<255 && self.obj.cuantificar=='SI'){
                    quantifie();
                }else{
                    AddAlert("success", "Proceso terminado correctamente");
                    ocultarModal();
                    //$( "#portfolio" ).scroll();
                    scrollToAnchor('portfolio');
                }
            },
            error: errorPeticion
        });
    }
    //5
    function quantifie(){
        modalEsperaTitulo("Cuantificando el holograma...");
        $("#portfolio-cuantificado").css("display","block");
        $.ajax({
            type:"POST",
            url: '/hologramme_quantifie/calculer',
            data: JSON.stringify(self.obj),
            contentType: "application/json; charset=utf-8",
            dataType: 'json',
            success: function(data){
                AddAlert("success", "Proceso terminado correctamente")
                ocultarModal();
                scrollToAnchor('portfolio-cuantificado');
                $( "#portfolio-cuantificado" ).scroll();
                $("#reconstruccion-cuantificado").attr("src",data.reconstruccion);
                $("#holograma-cuantificado").attr("src",data.holograma);
                $("#cuantificado-eqm").html(data.cuantificadoEqm);
                $("#cuantificado-ed").html(data.cuantificadoEd);
                $("#cuantificado-rsb").html(data.cuantificadoRsb);
                $("#cuantificado-u").html(data.cuantificadoU);
                $("#cuantificado-zb").html(data.cuantificadoZb);
                $("#cuantificado-ds").html(data.cuantificadoDs);
                enlacesDescargarReconstruir("#descargar-reconstruccion-cuantificado",data.enlaceReconstruir);
                enlacesDescargarHolo("#descargar-holograma-cuantificado",data.enlaceHolograma);
            },
            error: errorPeticion
        });
    }

    function scrollToAnchor(aid){
        var tag = $("#"+aid+"");
        $('html,body').animate({scrollTop: tag.offset().top},'slow');
    };
    function aplicacionOptica(valor){
        if(valor){
            self.obj.aplicacion_optica = "SI";
            self.obj.phase = 'phaheur';
            self.obj.phaseinitial = 'bandelimitee';
            $("#tailleobject").prop("disabled",false);
        }else{
            self.obj.aplicacion_optica = "NO";
            self.obj.phase = 'phasealea';
            self.obj.phaseinitial = 'pasbandelimite';
            
            self.obj.tailleobject = self.obj.tailleimg;

            $("#tailleobject").val(self.obj.tailleimg);
            $("#tailleobject").prop("disabled",true);
        }
        document.formulario.aplicacion_optica.value = self.obj.aplicacion_optica;
        document.formulario.phase.value = self.obj.phase;
        document.formulario.phaseinitial.value = self.obj.phaseinitial;
    }
    function cuantificarHolograma(cuantificar){
        if(cuantificar){
            $(".cuantificar").css('display','block');
            self.obj.cuantificar = "SI";
            $('#niveaux').prop("disabled",false);
            $("#niveaux").prop("required", true);
        }else{
            $(".cuantificar").css('display','none');
            self.obj.cuantificar = "NO";
            $('#niveaux').prop("disabled",true);
            $("#niveaux").removeProp("required");
        }
        document.formulario.cuantificar.value = self.obj.cuantificar;
    };
    function enlacesDescargarHolo(id,links){
        $(id).empty();
        $.each(links,function(index,item){
            $(id).append("<li><a href='" + item.url + "' download>"+item.tipo+"</a></li>");
        });
    }
    //
    function enlacesDescargarReconstruir(id,links){
        $(id).empty();
        $.each(links,function(index,item){
            $(id).append("<li><a href='" + item.url + "' download>"+item.tipo+"</a></li>");
        });
    }
    function errorPeticion(error){
        console.log(error);
        var response = error.responseJSON?error.responseJSON.error:error.responseText;
        if(response==null){
            response = "No se pudo procesar la solicitud, por favor intentelo más tarde";
        }
        if(response.length>100){
            response = "No se pudo procesar la solicitud, por favor intentelo más tarde";
        }
        AddAlert("danger", response)
        ocultarModal();
    }

    function AddAlert(type, msg) {
        console.log(type);
        switch (type) {
            case "danger":
                toaster.options.timeOut = 100000;
                toaster.error(msg, "HoloEasy - Error");
                break;
            case "warning":
                toaster.options.timeOut = 6000;
                toaster.warning(msg, "HoloEasy - Advertencia");
                break;
            case "success":
                toaster.options.timeOut = 3000;
                toaster.success(msg, "HoloEasy - Completado");
                break;
        }
    };
}

var app = new HoloEasy();