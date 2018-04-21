"use strict";

var objeto = {
  beamShaping : {
      tipoimg : 'carre',
      tipoilum : 'carre',
      phase : 'phaheur',
      phaseinitial : 'bandelimitee',
      aplicacion_optica : 'SI',
      cuantificar : 'SI',
      optimiserODD : 1,
      phasealea : 0,
      phaheur : 1,
      phaspher : 0,
      phawyr : 0,
      optimiser : 1,
      code : 'codedoux',//codedoux,codedur
      tailleimg : 64,
      pixelmargin : 0,
      tailleobject : 64,
      MASIRdes : 0.8,
      iterODD : 100,
      taillesignal : 128,
      tailleholo : 64,
      iteropt : 50,
      lissage2 : 0.8,
      iteranalog : 20,
      PRs : 1,
      PRb : 0,
      DPRA : 1,
      DPLRA : 0,
      DPE : 0,
      niveaux : 4,
      iterquantization : 20,
      diffphase : 1.335,
      controlbande : 0.01,
      masirREF : 10,
      iteranalogo : 20,
      masirODD : 0,
      DSdiff : 0            
  },
  imagenes : {
      imagen1 : undefined,
      imagen2 : undefined,
      imagen3 : undefined,
      imagen3 : undefined,
      imagen4 : undefined,
      imagen5 : undefined,
      imagen6 : undefined,
      imagen7 : undefined,
      imagen8 : undefined
  }
};


toaster.options = {
    "closeButton": true,
    "debug": false,
    "newestOnTop": false,
    "progressBar": false,
    "positionClass": "toast-bottom-full-width",
    "preventDuplicates": false,
    "onclick": null,
    "showDuration": "300",
    "hideDuration": "500",
    "timeOut": "10000",
    "extendedTimeOut": "10000",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
};