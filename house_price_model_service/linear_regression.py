# Copyright 2016 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Linear regression using the LinearRegressor Estimator."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf

import importData # pylint: disable=g-bad-import-order

STEPS = 1000
PRICE_NORM_FACTOR = 1000


def main(argv):
  """Builds, trains, and evaluates the model."""
  assert len(argv) == 1
  (train, test) = importData.dataset()

  # Switch the labels to units of thousands for better convergence.
  def to_thousands(features, labels):
    return features, labels/PRICE_NORM_FACTOR

  train = train.map(to_thousands)
  test = test.map(to_thousands)

  # Build the training input_fn.
  def input_train():
    return (
        # Shuffling with a buffer larger than the data set ensures
        # that the examples are well mixed.
        train.shuffle(1000).batch(128)
        # Repeat forever
        .repeat().make_one_shot_iterator().get_next())

  # Build the validation input_fn.
  def input_test():
    return (test.shuffle(1000).batch(128)
            .make_one_shot_iterator().get_next())

  feature_columns = [
      tf.feature_column.numeric_column(key="flooring"),
      tf.feature_column.numeric_column(key="fencing"),
      tf.feature_column.numeric_column(key="baths"),
      tf.feature_column.numeric_column(key="beds"),
      tf.feature_column.numeric_column(key="zip_code"),
      tf.feature_column.numeric_column(key="built_yr"),
      tf.feature_column.numeric_column(key="gutters"),
      tf.feature_column.numeric_column(key="sqft")
  ]

  # Build the Estimator.
  model = tf.estimator.LinearRegressor(feature_columns=feature_columns)

  # Train the model.
  # By default, the Estimators log output every 100 steps.
  model.train(input_fn=input_train, steps=STEPS)

  # Evaluate how the model performs on data it has not yet seen.
  eval_result = model.evaluate(input_fn=input_test)

  # The evaluation returns a Python dictionary. The "average_loss" key holds the
  # Mean Squared Error (MSE).
  average_loss = eval_result["average_loss"]

  # Convert MSE to Root Mean Square Error (RMSE).
  print("\n" + 80 * "*")
  print("\nRMS error for the test set: ${:.0f}"
        .format(PRICE_NORM_FACTOR * average_loss**0.5))

  # Run the model in prediction mode.
  input_dict = {
      "flooring": np.array([4]),
      "fencing": np.array([0]),
      "baths": np.array([2]),
      "beds": np.array([3]),
      "zip_code": np.array([75035]),
      "built_yr": np.array([1998]),
      "gutters": np.array([0]),
      "sqft": np.array([2000])
  }
  predict_input_fn = tf.estimator.inputs.numpy_input_fn(
      input_dict, shuffle=False)
  predict_results = model.predict(input_fn=predict_input_fn)

  # Print the prediction results.
  print("\nPrediction results:")
  for i, prediction in enumerate(predict_results):
    msg = ("flooring: {: 4d}, "
           "fencing: {: 4d}, "
           "baths: {: 4d}, "
           "beds: {: 4d}, "
           "zip_code: {: 4d}, "
           "built_yr: {: 4d}, "
           "Prediction: ${: 9.2f}")
    msg = msg.format(input_dict["flooring"][i], input_dict["fencing"][i],input_dict["baths"][i],input_dict["beds"][i],input_dict["zip_code"][i],input_dict["built_yr"][i],
                     PRICE_NORM_FACTOR * prediction["predictions"][0])

    print("    " + msg)
  print()


if __name__ == "__main__":
  # The Estimator periodically generates "INFO" logs; make these logs visible.
  tf.logging.set_verbosity(tf.logging.INFO)
  tf.app.run(main=main)