from lib import fn
from lib import File
from lib import DebugManager

import nltk
import re
import pandas as pd
import string
import numpy as np
import datetime
from datetime import datetime, timedelta
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
import sys
import os;
from importlib import resources


### william comment
def mergeFilterRaw(group_infor, store_code, country, share_drive):
	Debug = DebugManager.DebugManager();
	Debug.start();
	Debug.trace('start');
	folder_path = "{0}中国资料$/1) ALL Purchasing/39) William Cheah/transaction data/{1}".format(share_drive, country.lower())
	mas_stock_path = "{0}/raw_data/analytics/{1}/{2}".format(ROOT_PATH, 'product_relation', country)

	df_list = []
	include_plucode = group_infor['include_plucode']
	date_time_list = group_infor['date_time_list']
	include_department = group_infor['include_department']
	exclude_department = group_infor['exclude_department']
	m_category = group_infor['m_category']

	store_code = [s.upper() for s in store_code]
	find_regex = tuple(string.punctuation)
	# print('folder_path', folder_path)
	# files = File.getFilesFromDir(folder_path)
	# Debug.trace('get all transaction files');

	### william comment
	trx_files = [];
	for date_time in date_time_list:
		# print('date_time', date_time)
		for part_no in range(1, 20):
			filepath = '{0}/{1}_transaction_{2}_{3}.csv'.format(folder_path, country.lower(), date_time, part_no);
			if os.path.exists(filepath) and filepath not in trx_files:
				trx_files.append(filepath);

	Debug.trace('get all transaction trx_files');

	mas_files = File.getFilesFromDir(mas_stock_path)

	for file in mas_files:
		filename = file.split('/')[-1]
		if 'mas_stock' in  filename.lower() and not filename.startswith(find_regex) and filename.endswith('.csv'):
			mas_stock_df = File.readCSVToDF(file)
			mas_stock_df = mas_stock_df.fillna('-')

	for file in trx_files:
		filename = file.split('/')[-1];
		df_transaction = File.readCSVToDF(file)

		if not df_transaction.empty:
			print('reading', filename)
			df_transaction = fn.renameDFColumn({'SDTL_PLUNO': 'M_PLUCODE', 'SDTL_STORE': 'STORE', 'SDTL_CLOSEDATE': 'CLOSEDATE', 'SDTL_QTY': 'SALES_QTY'}, df_transaction)
			df_transaction = df_transaction.dropna(subset = ['M_PLUCODE', 'SDTL_CTRNO', 'SDTL_TRANSNO', 'CLOSEDATE', 'STORE'])

			df_merge = df_transaction.merge(mas_stock_df, on=['M_PLUCODE'], how='left')

			# filter store code
			filter_df = df_merge[df_merge['STORE'].isin(store_code)]
			filter_df = fn.convertToNumeric(['SDTL_SEQNO', 'SALES_QTY', 'SDTL_NETPRICE', 'SDTL_DISCAMT', 'SDTL_UNITCOST'], filter_df)
			filter_df = fn.convertToDate(['CLOSEDATE'], filter_df)

			# filter plucode
			if include_plucode:
				filter_df = filter_df[filter_df['M_PLUCODE'].isin(include_plucode)]

			# filter department
			if include_department:
				filter_df = filter_df[filter_df['M_DEPARTMENT'].isin(include_department)]
			
			if exclude_department:
				filter_df = filter_df[~(filter_df['M_DEPARTMENT'].isin(exclude_department))]
			
			# filter category
			if m_category:
				filter_df = filter_df[filter_df['M_CATEGORY'].isin(m_category)]
			
			df_list.append(filter_df);

	if df_list:
		df = pd.concat(df_list)
		df_list = []; ### reduce memory usage
		df = fn.renameDFColumn({'SDTL_PLUNO': 'M_PLUCODE', 'SDTL_STORE': 'STORE', 'SDTL_CLOSEDATE': 'CLOSEDATE', 'SDTL_QTY': 'SALES_QTY'}, df)
		df = df.dropna(subset = ['M_PLUCODE', 'SDTL_CTRNO', 'SDTL_TRANSNO', 'CLOSEDATE', 'STORE'])

		# save all raw
		temp_path = "{0}/raw_data/analytics/{1}/{2}".format(ROOT_PATH, 'product_relation/temp', 'filter_raw.csv')
		File.writeToCsv(temp_path, df, chunksize=500000)
	else:
		temp_path = "{0}/raw_data/analytics/{1}/{2}".format(ROOT_PATH, 'product_relation/temp', 'filter_raw.csv')
	return temp_path;



def mergeAllRaw(group_infor, country, share_drive):
	folder_path = "{0}中国资料$/1) ALL Purchasing/39) William Cheah/transaction data/{1}".format(share_drive, country.lower())
	mas_stock_path = "{0}/raw_data/analytics/{1}/{2}".format(ROOT_PATH, 'product_relation', country)

	Debug = DebugManager.DebugManager();
	Debug.start();
	Debug.trace('start');
	
	df_list = []
	include_plucode = group_infor['include_plucode']
	date_time_list = group_infor['date_time_list']
	include_department = group_infor['include_department']
	exclude_department = group_infor['exclude_department']
	m_category = group_infor['m_category']

	store_code = [s.upper() for s in store_code]
	find_regex = tuple(string.punctuation)

	### william comment
	trx_files = [];
	for date_time in date_time_list:
		# print('date_time', date_time)
		for part_no in range(1, 20):
			filepath = '{0}/{1}_transaction_{2}_{3}.csv'.format(folder_path, country.lower(), date_time, part_no);
			if os.path.exists(filepath) and filepath not in trx_files:
				trx_files.append(filepath);

	Debug.trace('get all transaction trx_files');

	mas_files = File.getFilesFromDir(mas_stock_path)

	for file in mas_files:
		filename = file.split('/')[-1]
		if 'mas_stock' in  filename.lower() and not filename.startswith(find_regex) and filename.endswith('.csv'):
			mas_stock_df = File.readCSVToDF(file)
			mas_stock_df = mas_stock_df.fillna('-')
	
	### william comment
	for file in trx_files:
		filename = file.split('/')[-1];
		print(filename)
		df_transaction = File.readCSVToDF(file)
		df_list.append(df_transaction)		
	Debug.trace('read transaction & master files');
	
	if df_list:
		
		df = pd.concat(df_list)
		df_list = []; ### reduce memory usage
		df = fn.renameDFColumn({'SDTL_PLUNO': 'M_PLUCODE', 'SDTL_STORE': 'STORE', 'SDTL_CLOSEDATE': 'CLOSEDATE', 'SDTL_QTY': 'SALES_QTY'}, df)
		df = df.dropna(subset = ['M_PLUCODE', 'SDTL_CTRNO', 'SDTL_TRANSNO', 'CLOSEDATE', 'STORE'])

		df_merge = df.merge(mas_stock_df, on=['M_PLUCODE'], how='left')

		# save all raw
		temp_path = "{0}/raw_data/analytics/{1}/{2}".format(ROOT_PATH, 'product_relation/temp', 'all_raw.csv')
		File.writeToCsv(temp_path, df_merge, chunksize=500000)
	else:
		print('Dataframe list is empty in mergeAllRaw.')
		sys.exit()
	return df_merge;

def processRaw(raw_file, group_infor, store_code):
	include_plucode = group_infor['include_plucode']
	date_time_list = group_infor['date_time_list']
	include_department = group_infor['include_department']
	exclude_department = group_infor['exclude_department']
	m_category = group_infor['m_category']
	store_code = [s.upper() for s in store_code]

	raw_df = File.readCSVToDF(raw_file);
	
	if not raw_df.empty:
		# filter store code
		filter_df = raw_df[raw_df['STORE'].isin(store_code)]
		filter_df = fn.convertToNumeric(['SDTL_SEQNO', 'SALES_QTY', 'SDTL_NETPRICE', 'SDTL_DISCAMT', 'SDTL_UNITCOST'], filter_df)
		filter_df = fn.convertToDate(['CLOSEDATE'], filter_df)

		# filter plucode
		if include_plucode:
			filter_df = filter_df[filter_df['M_PLUCODE'].isin(include_plucode)]

		# filter department
		if include_department:
			filter_df = filter_df[filter_df['M_DEPARTMENT'].isin(include_department)]
		
		if exclude_department:
			filter_df = filter_df[~(filter_df['M_DEPARTMENT'].isin(exclude_department))]
		
		# filter category
		if m_category:
			filter_df = filter_df[filter_df['M_CATEGORY'].isin(m_category)]

		# save filter raw
		temp_path2 = "{0}/raw_data/analytics/{1}/{2}".format(ROOT_PATH, 'product_relation/temp', 'filter_raw.csv')
		File.writeToCsv(temp_path2, filter_df)
	else:
		temp_path2 = "{0}/raw_data/analytics/{1}/{2}".format(ROOT_PATH, 'product_relation/temp', 'filter_raw.csv')
	return temp_path2;

def transformData(filter_file, level = 'M_PLUCODE'):
	df_merge = File.readCSVToDF(filter_file);
	if not df_merge.empty:
		df_merge = fn.convertToDate(['CLOSEDATE'], df_merge)
		df_merge = fn.convertToNumeric(['SDTL_SEQNO', 'SALES_QTY', 'SDTL_NETPRICE', 'SDTL_DISCAMT', 'SDTL_UNITCOST'], df_merge)
		df_merge = df_merge[df_merge['SALES_QTY']>0]
		
		group_by = ['CLOSEDATE', level, 'SDTL_CTRNO', 'SDTL_TRANSNO', 'STORE']
		aggfunc = {'SALES_QTY': np.sum }
		
		df_pivot = fn.generatePivotTable(df_merge, group_by, aggfunc)
		df_pivot = df_pivot[(df_pivot[level] != '-')]
		# print(df_pivot)
		# temp_path = "{0}/raw_data/analytics{1}/{2}".format(ROOT_PATH, 'product_relation/temp', 'pivot_2.csv')
		# File.writeToCsv(temp_path, df_pivot)

		df_pivot['SKU_SPACE'] = df_pivot[level] + ' ';
		df_pivot['UNI_KEY'] = df_pivot['CLOSEDATE']+ '|' + df_pivot['STORE'] + '|' + df_pivot['SDTL_CTRNO'] + '|' + df_pivot['SDTL_TRANSNO'];
		group_by = ['UNI_KEY'];
		aggfunc = {
			'SKU_SPACE': sum,
		};
		concate_df = fn.generatePivotTable(df_pivot, group_by, aggfunc)
		concate_df = fn.renameDFColumn({'SKU_SPACE': level}, concate_df)

		concate_df = concate_df.dropna(subset = [level])
		concate_df = concate_df.drop_duplicates()
		temp_path = "{0}/raw_data/analytics/{1}/{2}".format(ROOT_PATH, 'product_relation/temp', 'concate.csv')
		File.writeToCsv(temp_path, concate_df);
	else:
		temp_path = "{0}/raw_data/analytics/{1}/{2}".format(ROOT_PATH, 'product_relation/temp', 'concate.csv')
	return temp_path;

def applyApriori(transform_file, country, filter_file, level = 'M_PLUCODE', minsup = 0.015):
	concate_df = File.readCSVToDF(transform_file)
	filter_df = File.readCSVToDF(filter_file)

	if not concate_df.empty:

		# split plucode into list of list
		tokenize = list(concate_df.apply(lambda x: nltk.word_tokenize(x[level]),axis=1))

		te = TransactionEncoder()
		te_array = te.fit(tokenize).transform(tokenize)
		encoder_df = pd.DataFrame(te_array, columns=te.columns_)

		frequent_item = apriori(encoder_df, min_support = minsup, use_colnames = True, verbose = 1, low_memory=True)
		frequent_item = frequent_item.sort_values(by='support', ascending=False)
		print(frequent_item)

		rules = association_rules(frequent_item, metric = 'lift', min_threshold=1)
		rules = rules.sort_values(['confidence', 'lift'], ascending = [False, False])
		
		# start cleaning process
		rules = cleanDataFrame(rules, filter_df, level)
		
		print(rules)
		temp_path = "{0}/raw_data/analytics/{1}/{2}".format(ROOT_PATH, 'product_relation', '{0}_apriori_result.csv'.format(country.upper()))
		File.writeToCsv(temp_path, rules)
		return temp_path;



def cleanDataFrame(rules, filter_df, level):
	
	rules['antecedents'] = rules['antecedents'].apply(lambda x: list(x)).apply(lambda x: ', '.join(x)).astype(str)
	rules['consequents'] = rules['consequents'].apply(lambda x: list(x)).apply(lambda x: ', '.join(x)).astype(str)

	uni_rules = rules[~(rules['antecedents'].str.contains(',') | rules['consequents'].str.contains(','))]
	multi_rules = rules[(rules['antecedents'].str.contains(',') | rules['consequents'].str.contains(','))]

	if level.upper() == 'M_PLUCODE':
		insert_columns = ['M_DEPARTMENT(A)', 'M_DEPARTMENT(B)', 'DEPT_NAME(A)', 'DEPT_NAME(B)', 
							'PRODUCT_DESC(A)', 'PRODUCT_DESC(B)', 'M_CATEGORY(A)', 'M_CATEGORY(B)', 'CATEGORY_NAME(A)', 'CATEGORY_NAME(B)']
		
		multi_rules[insert_columns] = '-'
		uni_rules['M_DEPARTMENT(A)'] = uni_rules['antecedents'].map(dict(zip(filter_df['M_PLUCODE'], filter_df['M_DEPARTMENT'])))
		uni_rules['M_DEPARTMENT(B)'] = uni_rules['consequents'].map(dict(zip(filter_df['M_PLUCODE'], filter_df['M_DEPARTMENT'])))

		uni_rules['DEPT_NAME(A)'] = uni_rules['antecedents'].map(dict(zip(filter_df['M_PLUCODE'], filter_df['DEPT_NAME'])))
		uni_rules['DEPT_NAME(B)'] = uni_rules['consequents'].map(dict(zip(filter_df['M_PLUCODE'], filter_df['DEPT_NAME'])))

		uni_rules['PRODUCT_DESC(A)'] = uni_rules['antecedents'].map(dict(zip(filter_df['M_PLUCODE'], filter_df['PRODUCT_DESC'])))
		uni_rules['PRODUCT_DESC(B)'] = uni_rules['consequents'].map(dict(zip(filter_df['M_PLUCODE'], filter_df['PRODUCT_DESC'])))

		uni_rules['M_CATEGORY(A)'] = uni_rules['antecedents'].map(dict(zip(filter_df['M_PLUCODE'], filter_df['M_CATEGORY'])))
		uni_rules['M_CATEGORY(B)'] = uni_rules['consequents'].map(dict(zip(filter_df['M_PLUCODE'], filter_df['M_CATEGORY'])))

		uni_rules['CATEGORY_NAME(A)'] = uni_rules['antecedents'].map(dict(zip(filter_df['M_PLUCODE'], filter_df['CATEGORY_NAME'])))
		uni_rules['CATEGORY_NAME(B)'] = uni_rules['consequents'].map(dict(zip(filter_df['M_PLUCODE'], filter_df['CATEGORY_NAME'])))

	elif level.upper() == 'M_DEPARTMENT':

		insert_columns = ['DEPT_NAME(A)', 'DEPT_NAME(B)']
		multi_rules[insert_columns] = '-'

		uni_rules['DEPT_NAME(A)'] = uni_rules['antecedents'].map(dict(zip(filter_df['M_PLUCODE'], filter_df['DEPT_NAME'])))
		uni_rules['DEPT_NAME(B)'] = uni_rules['consequents'].map(dict(zip(filter_df['M_PLUCODE'], filter_df['DEPT_NAME'])))
	
	elif level.upper() == 'M_CATEGORY':

		insert_columns = ['CATEGORY_NAME(A)', 'CATEGORY_NAME(B)']
		multi_rules[insert_columns] = '-'

		uni_rules['CATEGORY_NAME(A)'] = uni_rules['antecedents'].map(dict(zip(filter_df['M_PLUCODE'], filter_df['CATEGORY_NAME'])))
		uni_rules['CATEGORY_NAME(B)'] = uni_rules['consequents'].map(dict(zip(filter_df['M_PLUCODE'], filter_df['CATEGORY_NAME'])))

	rules = pd.concat([uni_rules, multi_rules])

	return rules


def mergeMasStockProcess(folder_path, mas_stock_path, store_code, group_infor, country=None, share_drive=None):

	folder_path = "{0}中国资料$/1) ALL Purchasing/39) William Cheah/transaction data/{1}".format(share_drive, country.lower())
	mas_stock_path = "{0}/raw_data/{1}/{2}".format(ROOT_PATH, 'product_relation', country)

	Debug = DebugManager.DebugManager();
	Debug.start();
	Debug.trace('start');
	df_list = []
	include_plucode = group_infor['include_plucode']
	date_time_list = group_infor['date_time_list']
	include_department = group_infor['include_department']
	exclude_department = group_infor['exclude_department']
	m_category = group_infor['m_category']

	store_code = [s.upper() for s in store_code]
	find_regex = tuple(string.punctuation)
	# print('folder_path', folder_path)
	# files = File.getFilesFromDir(folder_path)
	# Debug.trace('get all transaction files');

	### william comment
	trx_files = [];
	for date_time in date_time_list:
		# print('date_time', date_time)
		for part_no in range(1, 20):
			filepath = '{0}/{1}_transaction_{2}_{3}.csv'.format(folder_path, country.lower(), date_time, part_no);
			if os.path.exists(filepath) and filepath not in trx_files:
				trx_files.append(filepath);

	Debug.trace('get all transaction trx_files');


	# print('mas_stock_path', mas_stock_path)
	mas_files = File.getFilesFromDir(mas_stock_path)

	for file in mas_files:
		filename = file.split('/')[-1]
		if 'mas_stock' in  filename.lower() and not filename.startswith(find_regex) and filename.endswith('.csv'):
			mas_stock_df = File.readCSVToDF(file)
			mas_stock_df = mas_stock_df.fillna('-')
	
	# for date_time in date_time_list:
	# 	for file in files:
	# 		filename = file.split('/')[-1]			
	# 		if 'transaction' in filename.lower():
	# 			if str(date_time) in filename and not filename.startswith(find_regex) and filename.endswith('.csv'):
	# 				print(filename)
	# 				df_transaction = File.readCSVToDF(file)
	# 				df_list.append(df_transaction)		

	### william comment
	for file in trx_files:
		filename = file.split('/')[-1];
		print(filename)
		df_transaction = File.readCSVToDF(file)
		df_list.append(df_transaction)		
	Debug.trace('read transaction & master files');
	
	if df_list:
		
		df = pd.concat(df_list)
		df_list = []; ### reduce memory usage
		df = fn.renameDFColumn({'SDTL_PLUNO': 'M_PLUCODE', 'SDTL_STORE': 'STORE', 'SDTL_CLOSEDATE': 'CLOSEDATE', 'SDTL_QTY': 'SALES_QTY'}, df)
		df = df.dropna(subset = ['M_PLUCODE', 'SDTL_CTRNO', 'SDTL_TRANSNO', 'CLOSEDATE', 'STORE'])

		df_merge = df.merge(mas_stock_df, on=['M_PLUCODE'], how='left')

		# save all raw
		temp_path = "{0}/raw_data/{1}/{2}".format(ROOT_PATH, 'product_relation/temp', 'all_raw.csv')
		File.writeToCsv(temp_path, df_merge)

		# filter store code
		filter_df = df_merge[df_merge['STORE'].isin(store_code)]
		filter_df = fn.convertToNumeric(['SDTL_SEQNO', 'SALES_QTY', 'SDTL_NETPRICE', 'SDTL_DISCAMT', 'SDTL_UNITCOST'], filter_df)
		filter_df = fn.convertToDate(['CLOSEDATE'], filter_df)

		# filter plucode
		if include_plucode:
			filter_df = filter_df[filter_df['M_PLUCODE'].isin(include_plucode)]

		# filter department
		if include_department:
			filter_df = filter_df[filter_df['M_DEPARTMENT'].isin(include_department)]
		
		if exclude_department:
			filter_df = filter_df[~(filter_df['M_DEPARTMENT'].isin(exclude_department))]
		
		# filter category
		if m_category:
			filter_df = filter_df[filter_df['M_CATEGORY'].isin(m_category)]

		# save filter raw
		temp_path2 = "{0}/raw_data/{1}/{2}".format(ROOT_PATH, 'product_relation/temp', 'filter_raw.csv')
		File.writeToCsv(temp_path2, filter_df)

		group_by = ['CLOSEDATE', 'M_PLUCODE', 'SDTL_CTRNO', 'SDTL_TRANSNO', 'STORE']
		aggfunc = {'SALES_QTY': np.sum }


		pivot_df = fn.generatePivotTable(filter_df, group_by, aggfunc)
		pivot_df = pivot_df.sort_values(by = ['SALES_QTY'], ascending = False)
		
		# save pivot table
		temp_path3 = "{0}/raw_data/{1}/{2}".format(ROOT_PATH, 'product_relation/temp', 'filter_pivot.csv')
		File.writeToCsv(temp_path3, pivot_df)

	else:
		print('Dataframe list is empty in mergeMasStockProcess.')
		sys.exit()
	Debug.end();
	Debug.show('mergeMasStockProcess');


def hot_encode(x):
    if(int(x)<= 0):
        return False
    if(int(x)>= 1):
        return True



def aprioriProcess(df_merge, df_pivot, date_time_list, level = 'M_PLUCODE', minsup = 0.015, refresh = False):

	Debug = DebugManager.DebugManager();
	Debug.start();
	Debug.trace('start');
	aprior_list = []
	
	df_merge = fn.convertToDate(['CLOSEDATE'], df_merge)
	df_merge = fn.convertToNumeric(['SDTL_SEQNO', 'SALES_QTY', 'SDTL_NETPRICE', 'SDTL_DISCAMT', 'SDTL_UNITCOST'], df_merge)
	df_merge = df_merge[df_merge['SALES_QTY']>0]
	
	group_by = ['CLOSEDATE', level, 'SDTL_CTRNO', 'SDTL_TRANSNO', 'STORE']
	aggfunc = {'SALES_QTY': np.sum }
	
	df_pivot = fn.generatePivotTable(df_merge, group_by, aggfunc)
	df_pivot = df_pivot[(df_pivot[level] != '-')]
	# print(df_pivot)
	temp_path = "{0}/raw_data/{1}/{2}".format(ROOT_PATH, 'product_relation/temp', 'pivot_2.csv')
	File.writeToCsv(temp_path, df_pivot)


	##################### old
	# df_pivot = fn.convertToDate(['CLOSEDATE'], df_pivot)
	# df_pivot = fn.convertToNumeric(['SALES_QTY'], df_pivot)

	# df_merge = fn.convertToDate(['CLOSEDATE'], df_merge)
	# df_merge = fn.convertToNumeric(['SALES_QTY', 'SDTL_NETPRICE'], df_merge)

	# df_merge = df_merge[df_merge['SALES_QTY']>0]
	# df_pivot = df_pivot[df_pivot['SALES_QTY']>0]
	
	
	# for date_time in date_time_list:
	# 	concate_dict = {}
	# 	concate_list = []
	# 	df_filter = df_pivot[df_pivot['CLOSEDATE'] == date_time]
	# 	df_dict = df_filter.to_dict('record')
		
	###########################

	############################ to open
	Debug.trace('df_merge');

	if refresh:
		# concate_dict = {}
		# concate_list = []
		# df_dict = df_pivot.to_dict('record')

		# for record in df_dict:
		# 	counter = record['SDTL_CTRNO']
		# 	number = record['SDTL_TRANSNO']
		# 	store = record['STORE']
		# 	date = record['CLOSEDATE']
		# 	uni_key = "{0}|{1}|{2}|{3}".format(date, store, counter, number)
		# 	extract_record = list(df_pivot[(df_pivot['SDTL_CTRNO'] == counter) & (df_pivot['SDTL_TRANSNO'] == number) & (df_pivot['STORE'] == store)][level].unique())
		# 	extract_record = ' '.join(extract_record)
		# 	concate_dict['UNI_KEY'] = uni_key
		# 	concate_dict[level] = extract_record
		# 	concate_list.append(concate_dict)
		# 	concate_dict = {}
		# 	extract_record = ''

		# concate_df = pd.DataFrame(concate_list)

		### william comment
		df_pivot['SKU_SPACE'] = df_pivot['M_PLUCODE'] + ' ';
		df_pivot['UNI_KEY'] = df_pivot['CLOSEDATE']+ '|' + df_pivot['STORE'] + '|' + df_pivot['SDTL_CTRNO'] + '|' + df_pivot['SDTL_TRANSNO'];
		group_by = ['UNI_KEY'];
		aggfunc = {
			'SKU_SPACE': sum,
		};
		concate_df = fn.generatePivotTable(df_pivot, group_by, aggfunc)
		concate_df = fn.renameDFColumn({'SKU_SPACE': level}, concate_df)

		concate_df = concate_df.dropna(subset = [level])
		concate_df = concate_df.drop_duplicates()
		temp_path = "{0}/raw_data/{1}/{2}".format(ROOT_PATH, 'product_relation/temp', 'concate.csv')
		File.writeToCsv(temp_path, concate_df)
	Debug.trace('summaries');
	##############################################

	temp_path = "{0}/raw_data/{1}/{2}".format(ROOT_PATH, 'product_relation/temp', 'concate.csv')
	concate_df = File.readCSVToDF(temp_path)

	# split plucode into list of list
	tokenize = list(concate_df.apply(lambda x: nltk.word_tokenize(x[level]),axis=1))

	te = TransactionEncoder()
	te_array = te.fit(tokenize).transform(tokenize)
	encoder_df = pd.DataFrame(te_array, columns=te.columns_)

	frequent_item = apriori(encoder_df, min_support = minsup, use_colnames = True, verbose = 1, low_memory=True)
	frequent_item = frequent_item.sort_values(by='support', ascending=False)
	# print(frequent_item)

	rules = association_rules(frequent_item, metric = 'lift', min_threshold=1)
	rules = rules.sort_values(['confidence', 'lift'], ascending = [False, False])
	
	rules['antecedents'] = rules['antecedents'].apply(lambda x: list(x)).apply(lambda x: ', '.join(x)).astype(str)
	rules['consequents'] = rules['consequents'].apply(lambda x: list(x)).apply(lambda x: ', '.join(x)).astype(str)
	print(rules)
	temp_path = "{0}/raw_data/{1}/{2}".format(ROOT_PATH, 'product_relation/temp', 'result.csv')
	File.writeToCsv(temp_path, rules)

	Debug.end()
	Debug.show('apriori process')
		

def run(params = {}):

	global ROOT_PATH
	ROOT_PATH = fn.getNestedElement(params, 'root_path')
	include_plucode = fn.getNestedElement(params, 'include_plucode')
	include_department = fn.getNestedElement(params, 'include_department')
	exclude_department = fn.getNestedElement(params, 'exclude_department')
	m_category = fn.getNestedElement(params, 'include_m_category')
	store_code = fn.getNestedElement(params, 'store_code', )
	start_date = fn.getNestedElement(params, 'start_date', '2022-10-01')
	end_date = fn.getNestedElement(params, 'end_date', '2022-10-07')
	country_list = fn.getNestedElement(params, 'country_list')
	share_drive = fn.getNestedElement(params, 'share_drive', 'Z:\\')
	level = fn.getNestedElement(params, 'level', 'M_PLUCODE')
	minsup = fn.getNestedElement(params, 'minsup', 0.015)
	refresh = fn.getNestedElement(params, 'refresh', False)
	process = fn.getNestedElement(params, 'process', ['merge_all_raw', 'filter_raw', 'transform', 'apriori'])

	Debug = DebugManager.DebugManager();
	Debug.start();
	Debug.trace('start')
	
	date_time_list = []        
	start_date = datetime.strptime(start_date,  '%Y-%m-%d').date()
	end_date = datetime.strptime(end_date,  '%Y-%m-%d').date()

	date_range = (end_date - start_date).days

	if date_range > 0:

		for i in range(0, date_range):
			date_time_gen = start_date + timedelta(days=i)
			date_time_list.append(str(date_time_gen))
	else:
		date_time_list.append(start_date)

	group_infor = {
					'include_plucode': include_plucode,
					'date_time_list': date_time_list,
					'include_department': include_department,
					'exclude_department': exclude_department,
					'm_category': m_category,
				}
		
	for country in country_list:

		### william comment
		# if refresh:
		# 	raw_df = mergeAllRaw(group_infor, country, share_drive)
		# 	processRaw(raw_file=None, raw_df=raw_df, group_infor=group_infor, store_code=store_code);

		# else:
		# 	all_raw_path = "{0}/raw_data/analytics/{1}/{2}".format(ROOT_PATH, 'product_relation/temp', 'all_raw.csv');
		# 	processRaw(raw_file=all_raw_path, raw_df=None, group_infor=group_infor, store_code=store_code);

		if 'merge_all_raw' in process:
			raw_file = mergeAllRaw(group_infor, country, share_drive)
		else:
			raw_file = "{0}/raw_data/analytics/{1}/{2}".format(ROOT_PATH, 'product_relation/temp', 'all_raw.csv');
		Debug.trace('merge_all_raw')

		if 'filter_raw' in process:
			filter_file = processRaw(raw_file=raw_file, raw_df=None, group_infor=group_infor, store_code=store_code);
		else:
			filter_file = "{0}/raw_data/analytics/{1}/{2}".format(ROOT_PATH, 'product_relation/temp', 'filter_raw.csv');
		Debug.trace('filter_raw')

		if 'merge_filter_raw' in process:
			filter_file = mergeFilterRaw(group_infor, store_code, country, share_drive);
		else:
			filter_file = "{0}/raw_data/analytics/{1}/{2}".format(ROOT_PATH, 'product_relation/temp', 'filter_raw.csv');
		Debug.trace('merge_filter_raw')

		if 'transform' in process:
			transform_file = transformData(filter_file, level)
		else:
			transform_file = "{0}/raw_data/analytics/{1}/{2}".format(ROOT_PATH, 'product_relation/temp', 'concate.csv');
		Debug.trace('transform')
		
		if 'apriori' in process:
			apriori_file = applyApriori(transform_file, country, filter_file, level=level, minsup=minsup);
		
		print('save', apriori_file)
		Debug.trace('apriori')

	Debug.end();
	Debug.show('product relation')





def testing():
	print('hi')
