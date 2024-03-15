import streamlit as st
from streamlit import session_state as state
from streamlit_option_menu import option_menu

import time

from utils import *


def check() -> None :
	check_register()
	check_login()

##################################################################################################################################
##################################################################################################################################
##################################################################################################################################

def check_register() :
	if state['register'] == True and state['logged_in'] == False :

		st.title('Регистрация')

		# Asking for a new handle, lowering it, and checking for its length
		new_handle = st.text_input('Пожалуйста, введите новый username :',
								   placeholder='Например: Qurbon_2000')
		new_handle = new_handle.lower()

		if new_handle != '' and ( len(new_handle) < 3 or len(new_handle) > 25 ) :
			st.error('Название аккаунта должно иметь больше 3-х и меньше 25-и символов!')
			st.stop()

		# Checking if such username already exists #

		for iter_ in get_docs( 'users_db' )['username'] :
			if iter_ == new_handle :
				st.error('Извините, такой аккаунт уже существует')
				st.stop()
		

		# Asking for the new password and checking its length #
		new_password = st.text_input('Пожалуйста, придумайте надежный пароль:',
									 placeholder='Убедитесь что никто не смотрит на вашу клавиатуру !', type='password')
		if new_password != '' and len(new_password) < 4 or len(new_password) > 25 :
			st.error('Пароль должен состоять из больше 3-х и меньше 25-и символов!')
			st.stop()

		# Waiting for the confirmation of the password #
		repeat_password = st.text_input('Пожалуйста, введите пароль раз:',placeholder='Пароли должны быть идентичны !',
										type='password')

		# If repeated password does not match the one from above #
		if repeat_password != '' and new_password != repeat_password :
			st.error('Пароли не совпадают !')
			st.stop()

		# Auth_code for registration (admins can create one) #
		auth_code = st.text_input('Введите токен (админ должен предоставить его) :',
								  placeholder='Токен меняется каждые 2 минуты !')

		# Checking whether it has letters or not #
		for i in auth_code :
			if i < '0' or i > '9' :
				st.error('Токен должен состоять только из чисел !')
				st.stop()


		# Checking if the auth_code been created #
		if len( str(get_doc('auth_code','self')['code']) ) == 0 and len(auth_code) > 0 :
			st.error('Токен не был создан !')
			st.stop()

		
		# Checking if the auth_code is valid #
		if str(get_doc('auth_code','self')['code']) != auth_code and len(auth_code) > 0 :
			st.error('Токены не совпадают !')
			st.stop()

		# Checking if auth_code is fresh (created at most 2 minute ago) #
		try :
			if time.time() - int(get_doc('auth_code','self')['time']) > 120 and len(auth_code) > 0 :

			   # Clearing the database #
				change_doc( 'auth_code','self',{'code':'','time':'','type':''} )
				st.error('Извините, срок токена истёк.')
				st.stop()
		except :
			print('Empty auth_code.')


		# Making sure that the user understands the risks #
		agreement = st.checkbox('Я понимаю что не смогу поменять свой username и свой пароль.')

		# Creating Submit and Login buttons #
		col1, col2 = st.columns(2)
		with col1 :
			if agreement == True and len(new_handle) > 0 and len(new_password) > 0 and new_password == repeat_password and len(auth_code) > 0 :
				submit_ = st.button('Продолжить')

				if submit_ == True :

					with st.spinner('Ждём...'):

						state['username'] = new_handle
						state['user_type'] = get_doc( 'auth_code','self' )['type']
						state['logged_in'] = True

						change_doc( 'users_db',new_doc_id('users_db'),
							{'username':new_handle, 'password':new_password, 'type': state['user_type'] } )

						change_doc( 'login_queries', new_doc_id('login_queries'),
							{ 'type':'register', 'username':state['username'], 'time': current_time() } )

						# Clearing auth_code #
						change_doc( 'auth_code','self',{'code':'','time':'','type':''} )

						st.success('Успешно зарегистрирован !')
						time.sleep(1)

						st.rerun()

		with col2 :
			login_ = st.button('Уже есть аккаунт ?')
			if login_ == True:
				state['register'] = False
				st.rerun()

			else : st.stop()


##################################################################################################################################
##################################################################################################################################
##################################################################################################################################


def check_login() :

	if state['logged_in'] == False and state['register'] == False :

		st.title('Login')

		# Asking for login and password #
		handle = st.text_input("Логин :", placeholder = "Пример : Qurbon_2000")
		handle = handle.lower()
		password = st.text_input('Пароль :',type='password',placeholder='Убедитесь что никто не смотрит на вашу клавиатуру !')

		# Asking to submit or register #
		col1, col2, col3, col4 = st.columns(4)

		with col1 :
			submit_ = st.button('Войти')
		with col4 :
			register = st.button('Создать аккаунт ?')
		
		# If clicks register button #
		if register == True:
			state['register'] = True
			with st.spinner('Подождите...'):
				time.sleep(1)
			st.rerun()


		elif submit_ == True :
			with st.spinner('Подождите...'):
				# Checking if the user exists in database #
				users_db = get_docs( 'users_db' )

				for i in range( len( users_db ) ) :
					if users_db['username'][i] == handle and users_db['password'][i] == password :
						state['user_found'] = True
						state['username'] = handle
						state['user_type'] = users_db['type'][i]


				# Checking if the user exists #
				if state['user_found'] == True and submit_ == True :

					state['logged_in'] = True

					change_doc( 'login_queries', new_doc_id('login_queries'),
								{ 'type':'login', 'username':state['username'], 'time': current_time() } )
					

					st.success('Вход выполнен !')
					time.sleep(1)

					st.rerun()

				elif handle != '' and password != '' and submit_ == True :
					st.error('Неправильный логин или пароль !')
					st.stop()

				else : st.stop()

		else : st.stop()