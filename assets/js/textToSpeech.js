// Configuração do Módulo
const config = {
    apiEndpoint: '/convert',
    maxRetries: 3,
    toastDuration: 3000,
    validationRules: {
        minLength: 1,
        maxLength: 50000
    }
};

// Interface para serviços
class TextToSpeechService {
    async convertText(text) {
        try {
            const response = await fetch(config.apiEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: text })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Erro na conversão');
            }

            return await response.blob();
        } catch (error) {
            throw new Error(`Erro na requisição: ${error.message}`);
        }
    }
}

// Classe para gerenciar UI
class UIManager {
    constructor(feedbackContainerId) {
        this.feedbackContainer = document.getElementById(feedbackContainerId);
    }

    showToast(message, type) {
        const toast = this.createToastElement(message, type);
        this.feedbackContainer.innerHTML = '';
        this.feedbackContainer.appendChild(toast);
        
        setTimeout(() => {
            toast.remove();
        }, config.toastDuration);
    }

    createToastElement(message, type) {
        const toast = document.createElement('div');
        toast.className = `toast show bg-${type} text-white`;
        toast.setAttribute('role', 'alert');
        
        const icon = this.getIconForType(type);
        
        toast.innerHTML = `
            <div class="toast-body">
                <i class="fas fa-${icon} me-2"></i>
                ${message}
            </div>
        `;
        
        return toast;
    }

    getIconForType(type) {
        const icons = {
            'success': 'check-circle',
            'danger': 'exclamation-circle',
            'info': 'info-circle'
        };
        return icons[type] || 'info-circle';
    }

    downloadBlob(blob, filename) {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        a.remove();
    }
}

// Classe para validação
class TextValidator {
    validate(text) {
        if (!text) {
            throw new Error('Por favor, insira um texto para converter.');
        }
        
        if (text.length > config.validationRules.maxLength) {
            throw new Error(`Texto muito longo. Máximo de ${config.validationRules.maxLength} caracteres.`);
        }

        return true;
    }
}

// Controlador principal
class TextToSpeechController {
    constructor() {
        this.service = new TextToSpeechService();
        this.ui = new UIManager('feedbackToast');
        this.validator = new TextValidator();
        this.form = document.getElementById('textToSpeechForm');
        this.setupEventListeners();
    }

    setupEventListeners() {
        this.form.addEventListener('submit', async (e) => {
            e.preventDefault();
            await this.handleSubmit(e);
        });
    }

    async handleSubmit(event) {
        const text = document.getElementById('inputText').value.trim();
        
        try {
            this.validator.validate(text);
            
            this.ui.showToast('Iniciando conversão...', 'info');
            
            const blob = await this.service.convertText(text);
            this.ui.downloadBlob(blob, 'Locucao.mp3');
            this.ui.showToast('Áudio gerado com sucesso!', 'success');
            
        } catch (error) {
            this.ui.showToast(error.message, 'danger');
            console.error('Erro:', error);
        }
    }
}

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    new TextToSpeechController();
});