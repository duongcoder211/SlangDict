// Упрощенный код для быстрой загрузки
document.addEventListener('DOMContentLoaded', function() {
    // Функция для эффекта появления при прокрутке
    const fadeElements = document.querySelectorAll('.fade-in');
    
    const fadeInOnScroll = function() {
        fadeElements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const elementVisible = 100;
            
            if (elementTop < window.innerHeight - elementVisible) {
                element.classList.add('visible');
            }
        });
    };
    
    fadeInOnScroll();
    window.addEventListener('scroll', fadeInOnScroll);
    
    // Плавная прокрутка
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 90,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Функция для эффекта качели 3D
    function createSwingEffect(element) {
        element.classList.add('swing-effect');
        
        element.addEventListener('mousemove', function(e) {
            // Получаем позицию курсора относительно центра элемента
            const rect = this.getBoundingClientRect();
            const centerX = rect.left + rect.width / 2;
            const centerY = rect.top + rect.height / 2;
            
            // Вычисляем расстояние от курсора до центра
            const deltaX = e.clientX - centerX;
            const deltaY = e.clientY - centerY;
            
            // Нормализуем значения от -1 до 1
            const normalizedX = deltaX / (rect.width / 2);
            const normalizedY = deltaY / (rect.height / 2);
            
            // Ограничиваем максимальный угол наклона
            const maxTilt = 8; // градусов
            
            // Вычисляем углы наклона
            // Ось Y вращает элемент по горизонтали (влево/вправо)
            // Ось X вращает элемент по вертикали (вверх/вниз)
            const rotateY = normalizedX * maxTilt;
            const rotateX = -normalizedY * maxTilt;
            
            // Применяем трансформацию
            this.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.02)`;
            
            // Добавляем тень для усиления эффекта глубины
            const shadowX = -normalizedX * 10;
            const shadowY = -normalizedY * 10;
            this.style.boxShadow = `${shadowX}px ${shadowY}px 20px rgba(0, 0, 0, 0.15)`;
        });
        
        element.addEventListener('mouseleave', function() {
            // Плавно возвращаем элемент в исходное состояние
            this.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale(1)';
            this.style.boxShadow = '0 15px 35px rgba(0, 0, 0, 0.15)';
        });
        
        element.addEventListener('mouseover', function() {
            // Небольшой эффект при наведении
            this.style.transform = 'perspective(1000px) scale(1.02)';
        });
    }
    
    // Применяем эффект ко всем карточкам и блоку about
    const cards = document.querySelectorAll('.feature-card, .about-project, .content-card');
    cards.forEach(card => {
        createSwingEffect(card);
    });
    
    // Демонстрация эффекта при загрузке
    // setTimeout(() => {
    //     const demoCard = document.querySelector('#card1');
    //     if (demoCard) {
    //         // Имитируем движение курсора по карточке
    //         demoCard.style.transform = 'perspective(1000px) rotateX(-4deg) rotateY(4deg) scale(1.02)';
    //         demoCard.style.boxShadow = '10px -10px 20px rgba(0, 0, 0, 0.15)';
            
    //         setTimeout(() => {
    //             demoCard.style.transform = 'perspective(1000px) rotateX(4deg) rotateY(-4deg) scale(1.02)';
    //             demoCard.style.boxShadow = '-10px 10px 20px rgba(0, 0, 0, 0.15)';
                
    //             setTimeout(() => {
    //                 demoCard.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale(1)';
    //                 demoCard.style.boxShadow = '0 15px 35px rgba(0, 0, 0, 0.15)';
    //             }, 600);
    //         }, 600);
    //     }
    // }, 1500);

    // DOM элементы
    const chatbotButton = document.getElementById('chatbotButton');
    const chatbotContainer = document.getElementById('chatbotContainer');
    const closeBtn = document.getElementById('closeBtn');
    const chatBody = document.getElementById('chatBody');
    const chatInput = document.getElementById('chatInput');
    const sendBtn = document.getElementById('sendBtn');

    // Переключение видимости чат-бота
    chatbotButton.addEventListener('click', () => {
        chatbotContainer.classList.toggle('active');
    });

    // Закрытие чат-бота
    closeBtn.addEventListener('click', () => {
        chatbotContainer.classList.remove('active');
    });

    // Отправка сообщения
    async function sendMessage() {
        const messageText = chatInput.value.trim();
        
        if (!messageText) return;
        
        // Добавляем сообщение пользователя
        addMessage(messageText, 'user');
        chatInput.value = '';
        
        // Показываем скелетон загрузки
        addSkeletonLoading();
        
        // Добавляем ответ от AI
        const aiResponse =  await getAIResponse(messageText);

        addMessage(aiResponse, 'bot');

        // Удаляем скелетон загрузки
        removeSkeletonLoading();
    }

    // Отправка сообщения при нажатии кнопки отправки
    sendBtn.addEventListener('click', sendMessage);

    // Отправка сообщения при нажатии Enter
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Добавление сообщения в чат
    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        // messageContent.textContent = text;
        // messageContent.textContent = marked.parse(`${text}`); // <p>The sum of 1 + 1 is <strong>2</strong>.</p>
        messageContent.innerHTML = marked.parse(`${text}`);
        
        const messageTime = document.createElement('div');
        messageTime.className = 'message-time';
        messageTime.textContent = getCurrentTime();
        
        messageDiv.appendChild(messageContent);
        messageDiv.appendChild(messageTime);
        
        chatBody.appendChild(messageDiv);
        
        // Прокручиваем вниз
        scrollToBottom();
    }

    // Добавление скелетона загрузки
    function addSkeletonLoading() {
        const skeletonDiv = document.createElement('div');
        skeletonDiv.className = 'skeleton-loading';
        skeletonDiv.id = 'skeletonLoading';
        skeletonDiv.textContent = 'Скоро будет готов ...';
        
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot';
        messageDiv.appendChild(skeletonDiv);
        
        chatBody.appendChild(messageDiv);
        
        // Прокручиваем вниз
        scrollToBottom();
    }

    // Удаление скелетона загрузки
    function removeSkeletonLoading() {
        const skeleton = document.getElementById('skeletonLoading');
        if (skeleton) {
            skeleton.parentElement.remove();
        }
    }

    // Получение текущего времени в формате ЧЧ:ММ
    function getCurrentTime() {
        const now = new Date();
        return `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;
    }

    // Прокрутка вниз чата
    function scrollToBottom() {
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    // Получение ответа от AI на основе сообщения
    async function getAIResponse(userMessage) {
        const message = { message: userMessage.toLowerCase()};

        try {
            const response = await fetch('/chat', {
                method: 'POST', // *GET, POST, PUT, DELETE, etc.
                headers: {
                    'Content-Type': 'application/json'
                    // Additional headers can be set here
                },
                body: JSON.stringify(message) // body data type must match "Content-Type" header
            })

            // Khi bạn dùng .then(), bạn cần return promise
            const data = await response.json() // Parses the JSON response into a JavaScript object
            // Прокручиваем вниз
            scrollToBottom();
            return data.response
            // console.log('Success:', data); // Handle the successful response data
        } catch (error){
            return "Ошибка произошла, попробуйте еще раз!"
            // console.error('Error:', error); // Handle errors during the fetch operation
        };
    }

    // Добавление нескольких примеров сообщений при загрузке страницы
    window.addEventListener('DOMContentLoaded', () => {
        // Приветственное сообщение уже есть в HTML
        // Добавляем еще одно сообщение для демонстрации
        setTimeout(() => {
            addMessage("Привет! Я AI ассистент. Чем я могу помочь вам сегодня?", 'bot');
            addMessage("Вы можете задать мне вопросы на любые темы. Я могу помочь с вопросами о технологиях, обучении или просто пообщаться!", 'bot');
        }, 1000);
    });
});
