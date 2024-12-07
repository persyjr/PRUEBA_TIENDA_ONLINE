import '/static/js/compressorjs.min.js';
import { LitElement, html, css, classMap } from '/static/js/lit.min.js';

export class WmImageField extends LitElement {
    static properties = {
        name: { type: String },
        label: { type: String },
        value: { type: Object },
        required: { type: Boolean },
        allowFiles: { type: Boolean },
        selectedResolution: {
            type: Object,
            state: true,
        },
        ogFile: { 
            type: Object,
            state: true,
        },
        isMobile: { 
            type: Boolean,
            state: true,
        },
        inputChecked: {
            type: Boolean,
            state: true,
        },
        url:{},
        noaplica: { type: Boolean },
    };

    static styles = [
        css`
            :host {
                display: block;
            }
        `
    ];

    constructor() {
        super();
        this.name = '';
        this.label = '';
        this.value = null;
        this.ogFile = null;
        this.isMobile = false;
        this.required = false;
        this.allowFiles = false;
        this.selectedResolution = { width: 1280, height: 720 };
        this.resolutions = [
            {width: 1920, height: 1080},
            {width: 2440, height: 1911},
        ];
        this.inputChecked = false;  
        this.url='';   
        this.noaplica = false;   
    }

    createRenderRoot() {
        return this;
    }

    render() {
        const { name, label, selectedResolution, value, isMobile, required, allowFiles, noaplica } = this; 

        return html`
            <div class="d-flex flex-column ">
                    ${!noaplica ? html`
                    <div class="d-flex flex-row justify-content-start ">
                        <div class="d-flex flex-row  align-self-start">                         
                            <label class="form-check-label pl-2" for="na_id_${name}">No Aplica</label><br>
                            <input class="ml-2" type="checkbox" @change=${this.setChecked} name="${name}-NA" id="na_id_${name}" >
                        </div>
                    </div>            
                    ` : ''}
                    
                    ${!!value && value.name !== 'False' && value.name !== 'NA.png' ? html`
                    <div class="ml-3">
                        <img src="${value.url}" id="id_NA" class="ml-3" style="height: 30px; width: 30px; border-radius: 50%; object-fit: cover;" alt="" >
                        <label for="${name}-clear_id">Limpiar Actual:</label>
                        <input type="checkbox" @change=${this.setClear} name="${name}-clear" id="${name}-clear_id">
                        <a   href="${value.url}"><p class="text-center" style="width: 170px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;direction: rtl;">${value.name}</p></a>
                    </div>
                        
                    ` : ''}
                </div>
                <div class="col " >
                    <div id="mobileUploadOptions" class="${classMap({'d-none': !isMobile})}">
                        <button type="button" class="btn btn-sm btn-primary" @click="${this.onCameraClicked}">Desde Camara</button>
                        <button type="button" class="btn btn-sm btn-secondary" @click="${this.onGalleryClicked}">Desde Galeria</button>
                    </div>
                    <div class="d-flex justify-content-center" >
                        <img id="img_prev_${name}" style="max-width:150px; object-fit: cover;">
                    </div>
                    <input type="file" id="file" accept="${allowFiles ? '*' : 'image/*'}" @change="${this.onFileChange}" name="${name}"
                        class="clearablefileinput form-control-file ${classMap({ 'd-none': isMobile })}" ?required=${required}>
                    <p class="text-muted m-0"><label>Resolución:AA</label> ${selectedResolution.width} x ${selectedResolution.height}</p>  
                </div>
        `;
    }
    
    setClear(event){
        const inputCurrent=$(`#na_id_${this.name}`).prop('checked', false);
        const inputFile=$(`input[name="${this.name}"]`).prop('value', '');
        inputFile.prop('required',false);
        

    }
    
    setChecked(event) {        
        const inputCurrent=$(`#${this.name}-clear_id`).prop('checked', false); 
        const inputFile=$(`input[name="${this.name}"]`).prop('value', '');        
        let identidad = `img_prev_${this.name}`
        let img = document.getElementById(identidad).parentElement;
        if (event.target.checked== true){
            inputFile.prop('required',false); 
            img.className="d-none"   
        }else{
            inputFile.prop('required',true);
            //img.className="d-flex justify-content-center"
            //onFileChange(event)
        }        
    }
    
    get fileInput() {
        return this.renderRoot.querySelector('#file');
    }

    connectedCallback() {
        super.connectedCallback();
        this.isMobile = this.isMobileDevice();
    }

    updated(chProps) {
        if (chProps.has('ogFile') || chProps.has('selectedResolution')) {
            this.compressFile(this.ogFile, this.selectedResolution);
        }
    } 
    mostrarImagen() {
        let file = this.fileInput.files[0];
        let reader = new FileReader();

        let name2=this.name
        reader.onload = function(e,name=name2) {
          let identidad = `img_prev_${name}`
          let img = document.getElementById(identidad);
          img.parentElement.className="d-flex justify-content-center"
          img.src= e.target.result;
        }
        reader.readAsDataURL(file);
      }
    onFileChange(e) {
        const inputCurrent=$(`#na_id_${this.name}`).prop('checked', false);        
        const inputClear=$(`input[name="${this.name}-clear"]`).prop('checked', false);
        this.ogFile = e.target.files[0];
        this.mostrarImagen()
    }

    
    onCameraClicked() {
        this.fileInput.accept = 'image/*';
        this.fileInput.capture = 'camera';
        this.fileInput.click();
        this.mostrarImagen()
    }

    onGalleryClicked() {
        this.fileInput.accept = 'image/*';
        this.fileInput.removeAttribute('capture');
        this.fileInput.click();
        this.mostrarImagen()
    }

    isMobileDevice = () => {
        return (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent));
    }

    compressFile(file, resolution) {
        if (!file) return;

        const input = this.fileInput;
        const maxRes = !!resolution ? { maxWidth: resolution.width, maxHeight: resolution.height } : {};
        new Compressor(file, {
            quality: 0.8,
            ...maxRes,

            success(result) {
                const compressedImageBlob = new Blob([result], { type: file.type });
                const compressedImageFile = new File([compressedImageBlob], file.name, { type: file.type });

                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(compressedImageFile);
                input.files = dataTransfer.files;
                console.info('compressed')
            },
            error(err) {
                console.error(err);
            },
        });
    }
}
customElements.define('wm-image-field', WmImageField);

 function agregar_imagen_circular() {
    let img=document.getElementById('id_NA')
    $('#id_NA').each(function(){
        if($(this)[0].naturalHeight == 0){
            $(this).attr('src','/media/FILEV1.png');
            img.setAttribute('src','/media/FILEV1.png')
    }
    });

    }
    $('#js-modal-3').on('show.bs.modal', function (event) { 
        setTimeout(() =>{
            agregar_imagen_circular()
    }, 100);
        
        });



    