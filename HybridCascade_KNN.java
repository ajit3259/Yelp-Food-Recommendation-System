package assinment1;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Set;

import weka.core.Attribute;
import weka.core.Instance;
import weka.core.Instances;
import weka.core.Debug.Random;
import weka.core.converters.ConverterUtils.DataSource;

public class research_project {

	public static Map<String, Double> sort(Map<String, Double> diff) {
		// 1. Convert Map to List of Map
		List<Map.Entry<String, Double>> list = new LinkedList<Map.Entry<String, Double>>(
				diff.entrySet());

		// 2. Sort list with Collections.sort(), provide a custom Comparator
		// Try switch the o1 o2 position for a different order
		Collections.sort(list, new Comparator<Map.Entry<String, Double>>() {
			public int compare(Map.Entry<String, Double> o1,
					Map.Entry<String, Double> o2) {
				return (o1.getValue()).compareTo(o2.getValue());
			}
		});

		// 3. Loop the sorted list and put it into a new insertion order Map
		// LinkedHashMap
		Map<String, Double> sortedMap = new LinkedHashMap<String, Double>();
		for (Map.Entry<String, Double> entry : list) {
			sortedMap.put(entry.getKey(), entry.getValue());
		}
		return sortedMap;
	}

	public static Map<String, Double> reverseSort(Map<String, Double> diff) {
		// 1. Convert Map to List of Map
		List<Map.Entry<String, Double>> list = new LinkedList<Map.Entry<String, Double>>(
				diff.entrySet());

		// 2. Sort list with Collections.sort(), provide a custom Comparator
		// Try switch the o1 o2 position for a different order
		Collections.sort(list, new Comparator<Map.Entry<String, Double>>() {
			public int compare(Map.Entry<String, Double> o1,
					Map.Entry<String, Double> o2) {
				return (o2.getValue()).compareTo(o1.getValue());
			}
		});

		// 3. Loop the sorted list and put it into a new insertion order Map
		// LinkedHashMap
		Map<String, Double> sortedMap = new LinkedHashMap<String, Double>();
		for (Map.Entry<String, Double> entry : list) {
			sortedMap.put(entry.getKey(), entry.getValue());
		}
		return sortedMap;
	}

	// Returns most similar user
	public static Map<String, Double> clusteringUser(Instances data,
			ArrayList<String> users, Instance test, String c) {

		Map<String, Double> average_ratings = new HashMap<String, Double>();
		Map<String, Integer> count = new HashMap<String, Integer>();
		for (String n : users) {
			for (int i = 0; i < data.numInstances(); i++) {
				int u = (int) data.instance(i).value(1);// user
				int b = (int) data.instance(i).value(6);// business
				int cat = (int) data.instance(i).value(0);// category

				if (data.attribute(1).value(u) == n
						&& data.attribute(0).value(cat) == c) {
					if (average_ratings.get(data.attribute(6).value(b)) == null) {
						average_ratings.put(data.attribute(6).value(b), data
								.instance(i).value(3));
						count.put(data.attribute(6).value(b), 1);
					} else {
						average_ratings.put(data.attribute(6).value(b),
								average_ratings.get(data.attribute(6).value(b))
										+ data.instance(i).value(3));
						count.put(data.attribute(6).value(b),
								count.get(data.attribute(6).value(b)) + 1);
					}
				}

			}
		}

		Map<String, Double> final_avg_value = new HashMap<String, Double>();
		for (String n : average_ratings.keySet()) {

			double temp = average_ratings.get(n) / count.get(n);
			final_avg_value.put(n, temp);

		}
		final_avg_value = reverseSort(final_avg_value);

		int i = 0;
		return final_avg_value;

	}

	// returning users belonging to same category to which test case belongs
	public static ArrayList<String> categ(Map<String, String> users,
			Instance k, Attribute a) {

		ArrayList<String> usr = new ArrayList<String>();
		for (String n : users.keySet()) {
			String value = users.get(n);
			int temp = (int) k.value(0);
			if (a.value(temp) == value)
				usr.add(n);
		}

		return usr;
	}

	public static String mode(Attribute a, ArrayList<Double> lis) {
		int max = 0;
		String value = null;
		for (int i = 0; i < a.numValues(); i++) {
			int count = 0;
			for (double n : lis) {
				int temp = (int) n;
				if (a.value(i) == a.value(temp)) {
					count++;
				}
			}
			if (count > max) {
				max = count;
				value = a.value(i);
			}
		}

		return value;

	}

	// tells which user has visited and rated which restaurant
	public static Map<String, ArrayList<Double>> trav(Instances data) {
		Map<String, ArrayList<Double>> vv = new HashMap<String, ArrayList<Double>>();

		for (int i = 0; i < data.attribute(1).numValues(); i++) {
			ArrayList<Double> tem = new ArrayList<Double>();
			for (int j = 0; j < data.numInstances(); j++) {
				int temp = (int) data.instance(j).value(1);

				if (data.attribute(1).value(temp) == data.attribute(1).value(i))

					tem.add(data.instance(j).value(0));
			}
			vv.put(data.attribute(1).value(i), tem);
		}

		return vv;
	}

	public static void main(String[] args) throws Exception {
		DataSource source = new DataSource("final_final_data.csv"); // load csv
		Instances data = source.getDataSet();
		// System.out.println(data);

		int folds = 10;
		Random rand = new Random();

		int seed = rand.nextInt(50) + 1;
		Random rand2 = new Random(seed);
		Instances randData = new Instances(data);
		randData.randomize(rand); // randomizing the normalized dataset
		Instances train = null; // initializing training dataset
		Instances test = null; // intitializing test dataset
		double avg_rmse = 0;
		for (int n = 0; n < folds; n++) {

			train = randData.trainCV(folds, n); // training dataset containg
												// k-1 folds in every
												// iteration
			test = randData.testCV(folds, n); // test dataset containing 1
												// fold in every iteration

			// getting the user cluster in form of arraylist
			Map<String, ArrayList<Double>> user_cluster_number = new HashMap<String, ArrayList<Double>>();
			Map<String, String> user_cluster_business = new HashMap<String, String>();
			Map<String, String> category_cluster = new HashMap<String, String>();

			ArrayList<String> temp = new ArrayList<String>();

			// tells which user has visited and rated which restaurant
			user_cluster_number = trav(train);

			// which type/category of restaurant a particular user has rated the
			// most

			for (String name : user_cluster_number.keySet()) {
				String category = null;
				ArrayList<Double> hel = new ArrayList<Double>();
				hel = user_cluster_number.get(name);
				int len = hel.size();
				if (len > 0) {
					category = mode(data.attribute(0), hel);
					user_cluster_business.put(name, category);
					// System.out.println(key + " " + hel);

				}
			}

			double rmse = 0;

			for (int j = 0; j < test.numInstances(); j++) {
				ArrayList<String> testing = new ArrayList<String>();
				testing = categ(user_cluster_business, test.instance(j),
						data.attribute(0));

				Map<String, Double> predict = new HashMap<String, Double>();
				// System.out.println(user_cluster_business);
				predict = clusteringUser(
						train,
						testing,
						test.instance(j),
						user_cluster_business.get(data.attribute(1).value(
								(int) train.instance(j).value(1))));
				for (String m : predict.keySet()) {
					if (m == data.attribute(6).value(
							(int) test.instance(j).value(6))) {
						System.out.println("r_cap:  " + predict.get(m));
						System.out.println("r:  " + test.instance(j).value(3));

						rmse = rmse
								+ Math.pow((predict.get(m) - test.instance(j)
										.value(3)), 2);

					}
				}
				// System.out.println(rmse);
			}
			// rmse =Math.sqrt(rmse/train.numInstances());
			// System.out.println(rmse);

		}

	}
}
