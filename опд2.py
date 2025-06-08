import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

logging.basicConfig(level=logging.INFO)

class MillionaireBot:
    def __init__(self, token: str):
        self.bot = Bot(token=token)
        self.storage = MemoryStorage()
        self.dp = Dispatcher(self.bot, storage=self.storage)

        self.GameStates = StatesGroup()
        self.GameStates.waiting_for_start = State()
        self.GameStates.question_1 = State()
        self.GameStates.question_2 = State()
        self.GameStates.question_3 = State()
        self.GameStates.question_4 = State()
        self.GameStates.question_5 = State()
        self.GameStates.game_over = State()

        self.questions = [
            {
                "question": "Дата крещения Руси?",
                "options": ["A) 2025", "B) 988", "C) 1991", "D) 992"],
                "correct": "B",
                "prize": "1,000"
            },
            {
                "question": "Сколько дней в високосном году??",
                "options": ["A) 364", "B) 365", "C) 366", "D) 360"],
                "correct": "B",
                "prize": "10,000"
            },
            {
                "question": "Столица России?",
                "options": ["A) Омск", "B) Питер", "C) Москва", "D) Астрахань"],
                "correct": "C",
                "prize": "100,000"
            },
            {
                "question": "В каком году был конец света'?",
                "options": ["A) 2020", "B) 2012", "C) 2004", "D) 2025"],
                "correct": "B",
                "prize": "500,000"
            },
            {
                "question": "Какой химический элемент обозначается как 'Au'?",
                "options": ["A) Серебро", "B) Железо", "C) Золото", "D) Алюминий"],
                "correct": "C",
                "prize": "1,000,000"
            }
        ]

        self.current_question = 0
        self.score = 0

        self.register_handlers()

    def get_start_keyboard(self):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton("Начать игру"))
        return keyboard

    def get_option_keyboard(self):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            types.KeyboardButton("A"),
            types.KeyboardButton("B"),
            types.KeyboardButton("C"),
            types.KeyboardButton("D")
        )
        return keyboard

    def register_handlers(self):
        @self.dp.message_handler(commands=['start'], state="*")
        async def cmd_start(message: types.Message):
            await self.GameStates.waiting_for_start.set()
            await message.answer(
                "Добро пожаловать в игру 'Кто хочет стать миллионером'!\n"
                "Правила просты: отвечайте на вопросы и выигрывайте деньги.\n"
                "Нажмите 'Начать игру', чтобы начать.",
                reply_markup=self.get_start_keyboard()
            )
        @self.dp.message_handler(text="Начать игру", state=self.GameStates.waiting_for_start)
        async def start_game(message: types.Message):
            self.current_question = 0
            self.score = 0
            await self.ask_question(message)

        for i in range(1, 6):
            state = getattr(self.GameStates, f'question_{i}')

            @self.dp.message_handler(state=state)
            async def handle_question(message: types.Message, state: FSMContext):
                await self.handle_answer(message, state)

    async def ask_question(self, message: types.Message):
        if self.current_question < len(self.questions):
            question_data = self.questions[self.current_question]
            question_text = (
                '\n'.join(question_data['options'])
            )

            await getattr(self.GameStates, f'question_{self.current_question + 1}').set()
            await message.answer(f"Вопрос за {question_data['prize']}:\n{question_data['question']}\n\n")
            await message.answer(question_text, reply_markup=self.get_option_keyboard())
        else:
            await self.GameStates.game_over.set()
            await message.answer(
                f"Поздравляем! Вы выиграли {self.questions[-1]['prize']} рублей!",
                reply_markup=types.ReplyKeyboardRemove()
            )

    async def handle_answer(self, message: types.Message, state: FSMContext):
        question_data = self.questions[self.current_question]
        user_answer = message.text.upper()

        if user_answer == question_data["correct"]:
            self.current_question += 1
            self.score = question_data["prize"]
            if self.current_question < len(self.questions):
                await message.answer(f"Правильно! Ваш текущий выигрыш: {self.score}")
                await self.ask_question(message)
            else:
                await self.GameStates.game_over.set()
                await message.answer(
                    f"Поздравляем! Вы выиграли {self.questions[-1]['prize']} рублей!",
                    reply_markup=types.ReplyKeyboardRemove()
                )
        else:
            await self.GameStates.game_over.set()
            if self.current_question > 0:
                lost_prize = self.questions[self.current_question - 1]["prize"]
            else:
                lost_prize = "0"
            await message.answer(
                f"Неправильно! Правильный ответ: {question_data['correct']}.\n"
                f"Ваш выигрыш: {lost_prize} рублей.",
                reply_markup=types.ReplyKeyboardRemove()
            )
    async def run(self):

        @self.dp.message_handler(state=self.GameStates.game_over)
        async def handle_game_over(message: types.Message, state: FSMContext):
            await message.answer(
                "Игра окончена. Хотите сыграть еще раз? Нажмите /start",
                reply_markup=types.ReplyKeyboardRemove()
            )
        await self.dp.start_polling()

async def main():
    bot = MillionaireBot("xxxxxxxxxxxxxxxxxxxxxx")
    await bot.run()

if __name__ == '__main__':
    import asyncio

    asyncio.run(main())