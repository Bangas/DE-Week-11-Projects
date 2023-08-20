# -*- coding: utf-8 -*-
"""Introduction to Unit Testing - Dennis Mutai

**Introduction to Unit Testing**

### **Background Information**

You are working on a project related to telecommunication billing data. As part of the project, a data pipeline has been provided to you. The data pipeline is responsible for extracting data from a CSV file, performing transformations using pandas, and storing the transformed data in another CSV file. Your task is to write unit tests for the functions in the data pipeline using the
unittest framework.

### **Problem Statement**

Your goal is to develop robust unit tests for the three functions in the data pipeline: data_extraction, data_transformation, and data_loading. These tests ensure the data pipeline functions correctly and handle various scenarios and edge cases.

### **Guidelines**

  ● Use the unittest framework to create test cases for each function in the data pipeline.

  ● Write at least three test cases for each function, covering different scenarios and edge cases.

  ● Ensure that your tests are independent and do not rely on each other.

  ● Name your test methods descriptively to indicate the scenario being tested.

  ● Use assertions to validate the expected behavior of each function.

  ● Provide informative error messages when assertions fail to aid in debugging.
"""

import pandas as pd
import unittest

def data_extraction(file_path):
    data = pd.read_csv(file_path)
    return data

def data_transformation(data):
    data = data.drop_duplicates()
    data['billing_amount'] = data['billing_amount'].str.replace('$', '').astype(float)
    data['total_charges'] = data['billing_amount'] + data['tax_amount']
    return data

def data_loading(data, output_file):
    data.to_csv(output_file, index=False)

class TestDataPipeline(unittest.TestCase):

    def setUp(billingdata):
        billingdata.file_path = 'billing_data.csv'
        billingdata.output_file = 'transformed_data.csv'

    def test_data_extraction(self):
        expected_data = pd.DataFrame({
            'customer_id': [1, 2, 3, 4, 5],
            'billing_amount': ['$100', '$200', '$300', '$400', '$500'],
            'tax_amount': [10, 20, 30, 40, 50]
        })
        #Test1: Ensure the data is correctly extracted from the input CSV file
        extracted_data = data_extraction(self.file_path)
        self.assertIsInstance(extracted_data, pd.DataFrame)
        self.assertEqual(len(extracted_data), 5)
        self.assertEqual(list(extracted_data.columns), ['customer_id', 'billing_amount', 'tax_amount'])
        self.assertTrue(expected_data.equals(extracted_data),
                        msg="Data extraction failed: The extracted data does not match the expected data.")

        #Test2: Empty  dataFrame when input csv is empty
        empty_file = 'empty_file.csv'
        extracted_data = data_extraction(empty_file)
        self.assertTrue(extracted_data.empty,
                        msg="Data extraction failed: An empty DataFrame was not returned for an empty input file.")

        # Test case 3: Exception is raised when the input file does not exist
        non_existing_file = 'non_existing_file.csv'
        with self.assertRaises(FileNotFoundError, msg="Data extraction failed: Expected FileNotFoundError"):
            data_extraction(non_existing_file)

        self.assertIsInstance(extracted_data, pd.DataFrame)
        self.assertEqual(len(extracted_data), 5)
        self.assertEqual(list(extracted_data.columns), ['customer_id', 'billing_amount', 'tax_amount'])

    def test_data_transformation(self):
        # Test case 1: Ensure the data is correctly transformed
        input_data = pd.DataFrame({
            'customer_id': [1, 2, 3, 4, 5],
            'billing_amount': ['$100', '$200', '$300', '$400', '$500'],
            'tax_amount': [10, 20, 30, 40, 50]
        })

        result = data_transformation(input_data)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 5)
        self.assertEqual(list(result.columns), ['customer_id', 'billing_amount', 'tax_amount', 'total_charges'])
        self.assertEqual(result['total_charges'].tolist(), [110, 220, 330, 440, 550])

        expected_transformed_data = pd.DataFrame({'customer_id': [1, 2, 3],
                                                  'total_amount': [110.0, 220.0, 165.0]})
        transformed_data = data_transformation(input_data)
        self.assertTrue(expected_transformed_data.equals(transformed_data),
                        msg="Data transformation failed: The transformed data does not match the expected data.")

        # Test case 2: Empty DataFrame is returned when the input data is empty
        empty_data = pd.DataFrame()
        transformed_data = data_transformation(empty_data)
        self.assertTrue(transformed_data.empty,
                        msg="Data transformation failed: An empty DataFrame was not returned for empty input data.")

        # Test case 3: Exception is raised when the required columns are missing in the input data
        missing_columns_data = pd.DataFrame({'customer_id': [1, 2, 3]})
        with self.assertRaises(KeyError, msg="Data transformation failed: Expected KeyError"):
            data_transformation(missing_columns_data)

    def test_data_loading(self):
      # Test case 1: Ensure the transformed data is correctly loaded into the output CSV file
        input_data = pd.DataFrame({
            'customer_id': [1, 2, 3],
            'billing_amount': [100, 200, 300],
            'tax_amount': [10, 20, 30],
            'total_charges': [110, 220, 330]
        })

        data_loading(input_data, self.output_file)

        result = pd.read_csv(self.output_file)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 3)
        self.assertEqual(list(result.columns), ['customer_id', 'billing_amount', 'tax_amount', 'total_charges'])
        self.assertEqual(result['total_charges'].tolist(), [110, 220, 330])

        input_data1 = pd.DataFrame({'customer_id': [1, 2, 3],
                                   'total_amount': [110.0, 220.0, 165.0]})
        data_loading(input_data1, self.output_file)
        loaded_data = pd.read_csv(self.output_file)
        self.assertTrue(input_data1.equals(loaded_data),
                        msg="Data loading failed: The loaded data does not match the input data.")

        # Test case 2: Ensure an exception is raised when the output file path is invalid
        invalid_output_file = '/content/file.csv'
        with self.assertRaises(FileNotFoundError, msg="Data loading failed: Expected FileNotFoundError"):
            data_loading(input_data, invalid_output_file)

        # Test case 3: Ensure the output file is created and empty when the input data is empty
        empty_data = pd.DataFrame()
        data_loading(empty_data, self.output_file)
        loaded_data = pd.read_csv(self.output_file)
        self.assertTrue(loaded_data.empty,
                        msg="Data loading failed: The loaded data is not empty when the input data is empty.")

if __name__ == '__main__':
    unittest.main(exit=False)
