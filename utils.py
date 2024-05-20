import pandas as pd
import numpy as np

import streamlit as st
from streamlit import session_state as state

from google.cloud import firestore

from datetime import datetime
import time

def read_file() :
    # Uploading file button #
    uploaded_file = st.file_uploader('')

    # Showing it to the user #
    # if uploaded_file != None and 'original_df' not in state :
        # Converting it to Pandas DataFrame #
        # original_df = pd.read_excel(uploaded_file) # Experimental
    
    if 'original_df' not in state :
        state['original_df'] = pd.read_excel('data.xlsx')
        state['preprocessed_df'] = state['original_df'].copy().reset_index(drop=True)


###############################################################

def indexed( data ) :
    data_copy = data.copy()
    data_copy.index = range( 1, len(data_copy) + 1 )
    return data_copy

def latest( data ) :
    try :
        data[state['base_date']] = pd.to_datetime(data['base_date'])
        data = data.sort_values('base_date',ascending=False)
    except :
        pass

    return data 

def current_time() :
    return pd.to_datetime( datetime.now() ).round('1s')


###############################################################
def space(num = 1):
	for _ in range(num) :
		st.write('')

def hr() :
    st.markdown("<hr>", unsafe_allow_html=True)

def side_hr() :
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)

###############################################################

def set_to_wide() :
	state['layout'] = 'wide'

def set_to_standard() :
	state['layout'] = 'centered'

################################################################

def arrange( df ) :
	st = set( df.columns )
	return st

def rearrange( df, collection_id ) :
	# Login queries #
	if collection_id == 'login_queries' :
		return df[ ['id','type', 'time', 'username'] ]

	# Users DB #
	if collection_id == 'users_db' :
		return df[ ['id','username','password','type', 'registered_at'] ]

################################################################
# Firestore Functions #
def get_docs( collection_id ) :

	try :
		docs =  state[collection_id].stream()
		items = list(map(lambda x: {**x.to_dict(), 'id': x.id}, docs))
		data = pd.DataFrame( items )

		data['id'] = data['id'].astype( 'int' )
		data = data.sort_values('id',ascending=False)
		data['id'] = data['id'].astype('str')

		data.index = range( len(data) )
		data = rearrange(data,collection_id)

		return data

	except :
		return pd.DataFrame()


def get_doc( collection_id, document_id ) :
	try :
		return state[collection_id].document(document_id ).get().to_dict()

	except :
		return state[collection_id]


def new_doc_id ( collection_id ) :
	try : mx = get_docs( collection_id )['id'].astype('int64').max()
	except : mx = 0

	return str( int(mx) + 1 )


def change_doc( collection_id, document_id, dict_values ) :
	state[collection_id].document( document_id ).set( dict_values )


def delete_doc( collection_id, document_id ) :
	state[collection_id].document( document_id ).delete()


def reset_( collection_id ) :
	docs = get_docs( collection_id )
	for i in docs['id'] :
		if i == '-1' :
			continue
		print( i )
		delete_doc( collection_id, i )

def reset_dbs() :
	# Initializing databases #
    with st.spinner( 'Deleting databases\' values' ) :
        databases_ = [ 'login_queries' ]
        for db in databases_ :
            reset_( db )
