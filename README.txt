
# Artifact Tool User Guide
ArtifactTool is a customizable tool that makes Artifact exploration easy and interactive.


```python
%matplotlib inline

import matplotlib.pyplot as plt

%run /homes/dingelsz/projects/artifact_tool/artifact_tool.py
```

## 1) Loading an Artifact:


```python
at = ArtifactTool('/share/scratch/users/abie/bfp_2.hdf')
```

## 2) Exploring an Artifact

Printing an artifact will give an overview of the structure of the underlying hdf:


```python
print(at)
```

    HDF: /share/scratch/users/abie/bfp_2.hdf
    ---Table Map---
    /dimensions/full_space
    /population/age_bins
    /population/structure
    /population/theoretical_minimum_risk_life_expectancy
    /risk_factor/child_stunting/exposure
    /risk_factor/child_stunting/relative_risk
    /risk_factor/child_underweight/exposure
    /risk_factor/child_underweight/relative_risk
    /risk_factor/child_wasting/exposure
    /risk_factor/child_wasting/relative_risk
    /risk_factor/discontinued_breastfeeding/exposure
    /risk_factor/discontinued_breastfeeding/relative_risk
    /risk_factor/non_exclusive_breastfeeding/exposure
    /risk_factor/non_exclusive_breastfeeding/relative_risk
    /population/structure/meta/values_block_1/meta
    /coverage_gap/low_hib_vaccine_coverage/exposure
    /coverage_gap/low_hib_vaccine_coverage/population_attributable_fraction
    /coverage_gap/low_hib_vaccine_coverage/relative_risk
    /coverage_gap/low_measles_vaccine_coverage_first_dose/exposure
    /coverage_gap/low_measles_vaccine_coverage_first_dose/population_attributable_fraction
    /coverage_gap/low_measles_vaccine_coverage_first_dose/relative_risk
    /covariate/live_births_by_sex/estimate
    /covariate/live_births_by_sex/estimate/meta/values_block_1/meta
    /cause/all_causes/cause_specific_mortality
    /cause/all_causes/death
    /cause/all_causes/excess_mortality
    /cause/all_causes/incidence
    /cause/all_causes/prevalence
    /cause/diarrheal_diseases/cause_specific_mortality
    /cause/diarrheal_diseases/death
    /cause/diarrheal_diseases/excess_mortality
    /cause/diarrheal_diseases/incidence
    /cause/diarrheal_diseases/population_attributable_fraction
    /cause/diarrheal_diseases/prevalence
    /cause/diarrheal_diseases/remission
    /cause/lower_respiratory_infections/cause_specific_mortality
    /cause/lower_respiratory_infections/death
    /cause/lower_respiratory_infections/excess_mortality
    /cause/lower_respiratory_infections/incidence
    /cause/lower_respiratory_infections/population_attributable_fraction
    /cause/lower_respiratory_infections/prevalence
    /cause/lower_respiratory_infections/remission
    /cause/measles/cause_specific_mortality
    /cause/measles/death
    /cause/measles/excess_mortality
    /cause/measles/incidence
    /cause/measles/population_attributable_fraction
    /cause/measles/prevalence



Each path represents a table in the HDF. Tables can be accessed using dot notation inside of the `tables` namespace. If you are unsure of the path to a table, tab completion inside jupyter/ipython will show you your availalbe options.


```python
at.tables.cause.measles.incidence.table().query('year == 2016 and age == 3 and sex == "Both"')
```




    array([[<matplotlib.axes._subplots.AxesSubplot object at 0x2aeeee1020b8>,
            <matplotlib.axes._subplots.AxesSubplot object at 0x2aeeeba63fd0>],
           [<matplotlib.axes._subplots.AxesSubplot object at 0x2aeeeba46b70>,
            <matplotlib.axes._subplots.AxesSubplot object at 0x2aeeeba2a780>]],
          dtype=object)




![png](output_7_1.png)



```python
del(at)
```

# GBDArtifactTool
The artifact tool can customized via subclasses to work with different artifacts.


```python
%run /homes/dingelsz/projects/artifact_tool/gbd_artifact_tool.py
```


```python
at = GBD_ArtifactTool('/share/scratch/users/abie/bfp_2.hdf')
```

## 1) Covariates


```python
at.covariates.ldi_income_per_capita(at.locations.Washington)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>model_version_id</th>
      <th>covariate_id</th>
      <th>covariate_name_short</th>
      <th>location_id</th>
      <th>location_name</th>
      <th>year_id</th>
      <th>age_group_id</th>
      <th>age_group_name</th>
      <th>sex_id</th>
      <th>mean_value</th>
      <th>lower_value</th>
      <th>upper_value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1950</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1421.241577</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>1</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1951</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1411.725708</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>2</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1952</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1401.770142</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>3</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1953</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1381.191284</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>4</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1954</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1372.482422</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>5</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1955</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1362.295410</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>6</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1956</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1350.799927</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>7</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1957</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1337.985596</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>8</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1958</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1331.504395</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>9</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1959</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1330.009277</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>10</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1960</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1336.568481</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>11</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1961</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1344.550659</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>12</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1962</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1341.008179</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>13</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1963</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1344.562988</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>14</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1964</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1356.927734</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>15</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1965</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1378.101440</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>16</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1966</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1399.377197</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>17</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1967</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1418.208740</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>18</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1968</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1444.185059</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>19</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1969</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1469.006592</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>20</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1970</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1498.877075</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>21</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1971</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1523.760498</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>22</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1972</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1551.396973</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>23</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1973</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1581.484253</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>24</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1974</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1603.465942</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>25</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1975</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1592.903076</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>26</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1976</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1583.734863</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>27</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1977</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1569.399658</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>28</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1978</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1555.081909</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>29</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1979</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1551.874512</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>37</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1987</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1522.364380</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>38</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1988</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1496.577637</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>39</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1989</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1456.435669</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>40</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1990</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1428.072754</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>41</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1991</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1407.230591</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>42</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1992</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1390.824219</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>43</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1993</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1382.022217</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>44</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1994</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1362.194458</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>45</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1995</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1355.629761</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>46</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1996</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1358.634888</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>47</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1997</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1371.801270</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>48</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1998</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1387.832764</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>49</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1999</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1411.558594</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>50</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>2000</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1442.236328</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>51</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>2001</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1476.026001</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>52</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>2002</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1514.234375</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>53</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>2003</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1551.081909</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>54</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>2004</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1589.499878</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>55</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>2005</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1618.117676</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>56</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>2006</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1641.370605</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>57</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>2007</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1665.529419</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>58</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>2008</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1690.196533</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>59</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>2009</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1707.345215</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>60</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>2010</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1715.591675</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>61</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>2011</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1720.140747</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>62</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>2012</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1729.269897</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>63</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>2013</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1749.078613</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>64</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>2014</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1779.950806</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>65</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>2015</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1816.642700</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>66</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>2016</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1856.089599</td>
      <td>None</td>
      <td>None</td>
    </tr>
  </tbody>
</table>
<p>67 rows × 12 columns</p>
</div>



## 2) Specialized Methods to work with specific artifacts


```python
print(help(at.reduce_draws))
```

    Help on method reduce_draws in module __main__:

    reduce_draws(table:pandas.core.frame.DataFrame, val_col:str='value') method of __main__.GBD_ArtifactTool instance
        Creates a DataFrame with mean and CI values obtained across draws.

        Parameters
        ----------
        table:
            A pandas DataFrame that contains a "draw" column
        col_name:
            The name of the column inside table that the mean and CI values should
            be computed from. The column should contain numeric values.

        Returns
        -------
        A table that summarizes key statistical values for a specific column

    None



```python
#table = at.tables.cause.diarrheal_diseases.incidence.table()
table = at.reduce_draws(table)
table
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>year</th>
      <th>location</th>
      <th>sex</th>
      <th>age</th>
      <th>value_mean</th>
      <th>lower 2.5</th>
      <th>upper 97.5</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1990</td>
      <td>Benin</td>
      <td>Both</td>
      <td>0.009589</td>
      <td>3.721025</td>
      <td>3.189655</td>
      <td>4.365909</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1990</td>
      <td>Benin</td>
      <td>Both</td>
      <td>0.047945</td>
      <td>3.586416</td>
      <td>3.111630</td>
      <td>4.177087</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1990</td>
      <td>Benin</td>
      <td>Both</td>
      <td>0.538356</td>
      <td>3.077102</td>
      <td>2.319018</td>
      <td>3.911503</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1990</td>
      <td>Benin</td>
      <td>Both</td>
      <td>3.000000</td>
      <td>2.865007</td>
      <td>2.224569</td>
      <td>3.517593</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1990</td>
      <td>Benin</td>
      <td>Both</td>
      <td>7.500000</td>
      <td>0.248775</td>
      <td>0.198380</td>
      <td>0.305901</td>
    </tr>
    <tr>
      <th>5</th>
      <td>1990</td>
      <td>Benin</td>
      <td>Both</td>
      <td>12.500000</td>
      <td>0.368012</td>
      <td>0.326431</td>
      <td>0.414143</td>
    </tr>
    <tr>
      <th>6</th>
      <td>1990</td>
      <td>Benin</td>
      <td>Both</td>
      <td>17.500000</td>
      <td>0.486656</td>
      <td>0.412351</td>
      <td>0.557660</td>
    </tr>
    <tr>
      <th>7</th>
      <td>1990</td>
      <td>Benin</td>
      <td>Both</td>
      <td>22.500000</td>
      <td>0.594474</td>
      <td>0.523377</td>
      <td>0.666461</td>
    </tr>
    <tr>
      <th>8</th>
      <td>1990</td>
      <td>Benin</td>
      <td>Both</td>
      <td>27.500000</td>
      <td>0.691704</td>
      <td>0.631559</td>
      <td>0.754457</td>
    </tr>
    <tr>
      <th>9</th>
      <td>1990</td>
      <td>Benin</td>
      <td>Both</td>
      <td>32.500000</td>
      <td>0.788407</td>
      <td>0.709392</td>
      <td>0.879006</td>
    </tr>
    <tr>
      <th>10</th>
      <td>1990</td>
      <td>Benin</td>
      <td>Both</td>
      <td>37.500000</td>
      <td>0.884388</td>
      <td>0.768382</td>
      <td>1.013634</td>
    </tr>
    <tr>
      <th>11</th>
      <td>1990</td>
      <td>Benin</td>
      <td>Both</td>
      <td>42.500000</td>
      <td>0.969298</td>
      <td>0.860721</td>
      <td>1.089452</td>
    </tr>
    <tr>
      <th>12</th>
      <td>1990</td>
      <td>Benin</td>
      <td>Both</td>
      <td>47.500000</td>
      <td>1.058391</td>
      <td>0.964761</td>
      <td>1.154919</td>
    </tr>
    <tr>
      <th>13</th>
      <td>1990</td>
      <td>Benin</td>
      <td>Both</td>
      <td>52.500000</td>
      <td>1.147687</td>
      <td>1.035736</td>
      <td>1.265844</td>
    </tr>
    <tr>
      <th>14</th>
      <td>1990</td>
      <td>Benin</td>
      <td>Both</td>
      <td>57.500000</td>
      <td>1.238757</td>
      <td>1.091623</td>
      <td>1.418741</td>
    </tr>
    <tr>
      <th>15</th>
      <td>1990</td>
      <td>Benin</td>
      <td>Both</td>
      <td>62.500000</td>
      <td>1.356821</td>
      <td>1.208184</td>
      <td>1.528222</td>
    </tr>
    <tr>
      <th>16</th>
      <td>1990</td>
      <td>Benin</td>
      <td>Both</td>
      <td>67.500000</td>
      <td>1.500792</td>
      <td>1.367624</td>
      <td>1.635892</td>
    </tr>
    <tr>
      <th>17</th>
      <td>1990</td>
      <td>Benin</td>
      <td>Both</td>
      <td>72.500000</td>
      <td>1.643048</td>
      <td>1.482017</td>
      <td>1.831092</td>
    </tr>
    <tr>
      <th>18</th>
      <td>1990</td>
      <td>Benin</td>
      <td>Both</td>
      <td>77.500000</td>
      <td>1.783393</td>
      <td>1.562550</td>
      <td>2.041581</td>
    </tr>
    <tr>
      <th>19</th>
      <td>1990</td>
      <td>Benin</td>
      <td>Both</td>
      <td>82.500000</td>
      <td>2.087649</td>
      <td>1.861222</td>
      <td>2.348657</td>
    </tr>
    <tr>
      <th>20</th>
      <td>1990</td>
      <td>Benin</td>
      <td>Both</td>
      <td>87.500000</td>
      <td>2.554639</td>
      <td>2.301751</td>
      <td>2.838671</td>
    </tr>
    <tr>
      <th>21</th>
      <td>1990</td>
      <td>Benin</td>
      <td>Both</td>
      <td>92.500000</td>
      <td>3.014778</td>
      <td>2.657701</td>
      <td>3.424057</td>
    </tr>
    <tr>
      <th>22</th>
      <td>1990</td>
      <td>Benin</td>
      <td>Both</td>
      <td>110.000000</td>
      <td>3.467388</td>
      <td>2.962337</td>
      <td>4.064540</td>
    </tr>
    <tr>
      <th>23</th>
      <td>1990</td>
      <td>Benin</td>
      <td>Female</td>
      <td>0.009589</td>
      <td>3.598227</td>
      <td>3.083219</td>
      <td>4.234391</td>
    </tr>
    <tr>
      <th>24</th>
      <td>1990</td>
      <td>Benin</td>
      <td>Female</td>
      <td>0.047945</td>
      <td>3.474790</td>
      <td>3.011689</td>
      <td>4.031913</td>
    </tr>
    <tr>
      <th>25</th>
      <td>1990</td>
      <td>Benin</td>
      <td>Female</td>
      <td>0.538356</td>
      <td>3.026055</td>
      <td>2.264103</td>
      <td>3.830818</td>
    </tr>
    <tr>
      <th>26</th>
      <td>1990</td>
      <td>Benin</td>
      <td>Female</td>
      <td>3.000000</td>
      <td>2.743477</td>
      <td>2.138389</td>
      <td>3.460993</td>
    </tr>
    <tr>
      <th>27</th>
      <td>1990</td>
      <td>Benin</td>
      <td>Female</td>
      <td>7.500000</td>
      <td>0.256235</td>
      <td>0.202245</td>
      <td>0.319334</td>
    </tr>
    <tr>
      <th>28</th>
      <td>1990</td>
      <td>Benin</td>
      <td>Female</td>
      <td>12.500000</td>
      <td>0.376544</td>
      <td>0.329798</td>
      <td>0.428981</td>
    </tr>
    <tr>
      <th>29</th>
      <td>1990</td>
      <td>Benin</td>
      <td>Female</td>
      <td>17.500000</td>
      <td>0.496258</td>
      <td>0.420658</td>
      <td>0.577638</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>384</th>
      <td>2016</td>
      <td>Benin</td>
      <td>Female</td>
      <td>67.500000</td>
      <td>1.411656</td>
      <td>1.266728</td>
      <td>1.561884</td>
    </tr>
    <tr>
      <th>385</th>
      <td>2016</td>
      <td>Benin</td>
      <td>Female</td>
      <td>72.500000</td>
      <td>1.531332</td>
      <td>1.338721</td>
      <td>1.735759</td>
    </tr>
    <tr>
      <th>386</th>
      <td>2016</td>
      <td>Benin</td>
      <td>Female</td>
      <td>77.500000</td>
      <td>1.650486</td>
      <td>1.385967</td>
      <td>1.946187</td>
    </tr>
    <tr>
      <th>387</th>
      <td>2016</td>
      <td>Benin</td>
      <td>Female</td>
      <td>82.500000</td>
      <td>1.919156</td>
      <td>1.664240</td>
      <td>2.205462</td>
    </tr>
    <tr>
      <th>388</th>
      <td>2016</td>
      <td>Benin</td>
      <td>Female</td>
      <td>87.500000</td>
      <td>2.332376</td>
      <td>2.060108</td>
      <td>2.632437</td>
    </tr>
    <tr>
      <th>389</th>
      <td>2016</td>
      <td>Benin</td>
      <td>Female</td>
      <td>92.500000</td>
      <td>2.740127</td>
      <td>2.341285</td>
      <td>3.159453</td>
    </tr>
    <tr>
      <th>390</th>
      <td>2016</td>
      <td>Benin</td>
      <td>Female</td>
      <td>110.000000</td>
      <td>3.142433</td>
      <td>2.565412</td>
      <td>3.751184</td>
    </tr>
    <tr>
      <th>391</th>
      <td>2016</td>
      <td>Benin</td>
      <td>Male</td>
      <td>0.009589</td>
      <td>3.296832</td>
      <td>2.742943</td>
      <td>3.895955</td>
    </tr>
    <tr>
      <th>392</th>
      <td>2016</td>
      <td>Benin</td>
      <td>Male</td>
      <td>0.047945</td>
      <td>3.172773</td>
      <td>2.686281</td>
      <td>3.701359</td>
    </tr>
    <tr>
      <th>393</th>
      <td>2016</td>
      <td>Benin</td>
      <td>Male</td>
      <td>0.538356</td>
      <td>2.537219</td>
      <td>2.018032</td>
      <td>3.133624</td>
    </tr>
    <tr>
      <th>394</th>
      <td>2016</td>
      <td>Benin</td>
      <td>Male</td>
      <td>3.000000</td>
      <td>1.971884</td>
      <td>1.593551</td>
      <td>2.424721</td>
    </tr>
    <tr>
      <th>395</th>
      <td>2016</td>
      <td>Benin</td>
      <td>Male</td>
      <td>7.500000</td>
      <td>0.281652</td>
      <td>0.216573</td>
      <td>0.359508</td>
    </tr>
    <tr>
      <th>396</th>
      <td>2016</td>
      <td>Benin</td>
      <td>Male</td>
      <td>12.500000</td>
      <td>0.392255</td>
      <td>0.337583</td>
      <td>0.451972</td>
    </tr>
    <tr>
      <th>397</th>
      <td>2016</td>
      <td>Benin</td>
      <td>Male</td>
      <td>17.500000</td>
      <td>0.502363</td>
      <td>0.420551</td>
      <td>0.593841</td>
    </tr>
    <tr>
      <th>398</th>
      <td>2016</td>
      <td>Benin</td>
      <td>Male</td>
      <td>22.500000</td>
      <td>0.593140</td>
      <td>0.503750</td>
      <td>0.690985</td>
    </tr>
    <tr>
      <th>399</th>
      <td>2016</td>
      <td>Benin</td>
      <td>Male</td>
      <td>27.500000</td>
      <td>0.664801</td>
      <td>0.594788</td>
      <td>0.741461</td>
    </tr>
    <tr>
      <th>400</th>
      <td>2016</td>
      <td>Benin</td>
      <td>Male</td>
      <td>32.500000</td>
      <td>0.736294</td>
      <td>0.650341</td>
      <td>0.828318</td>
    </tr>
    <tr>
      <th>401</th>
      <td>2016</td>
      <td>Benin</td>
      <td>Male</td>
      <td>37.500000</td>
      <td>0.807614</td>
      <td>0.687923</td>
      <td>0.951897</td>
    </tr>
    <tr>
      <th>402</th>
      <td>2016</td>
      <td>Benin</td>
      <td>Male</td>
      <td>42.500000</td>
      <td>0.873795</td>
      <td>0.755070</td>
      <td>1.015340</td>
    </tr>
    <tr>
      <th>403</th>
      <td>2016</td>
      <td>Benin</td>
      <td>Male</td>
      <td>47.500000</td>
      <td>0.934885</td>
      <td>0.839148</td>
      <td>1.046872</td>
    </tr>
    <tr>
      <th>404</th>
      <td>2016</td>
      <td>Benin</td>
      <td>Male</td>
      <td>52.500000</td>
      <td>0.995830</td>
      <td>0.879312</td>
      <td>1.127850</td>
    </tr>
    <tr>
      <th>405</th>
      <td>2016</td>
      <td>Benin</td>
      <td>Male</td>
      <td>57.500000</td>
      <td>1.056628</td>
      <td>0.899866</td>
      <td>1.251697</td>
    </tr>
    <tr>
      <th>406</th>
      <td>2016</td>
      <td>Benin</td>
      <td>Male</td>
      <td>62.500000</td>
      <td>1.167391</td>
      <td>1.016754</td>
      <td>1.350558</td>
    </tr>
    <tr>
      <th>407</th>
      <td>2016</td>
      <td>Benin</td>
      <td>Male</td>
      <td>67.500000</td>
      <td>1.327333</td>
      <td>1.194554</td>
      <td>1.472666</td>
    </tr>
    <tr>
      <th>408</th>
      <td>2016</td>
      <td>Benin</td>
      <td>Male</td>
      <td>72.500000</td>
      <td>1.486419</td>
      <td>1.311844</td>
      <td>1.690526</td>
    </tr>
    <tr>
      <th>409</th>
      <td>2016</td>
      <td>Benin</td>
      <td>Male</td>
      <td>77.500000</td>
      <td>1.644678</td>
      <td>1.384466</td>
      <td>1.920579</td>
    </tr>
    <tr>
      <th>410</th>
      <td>2016</td>
      <td>Benin</td>
      <td>Male</td>
      <td>82.500000</td>
      <td>1.935165</td>
      <td>1.676328</td>
      <td>2.196927</td>
    </tr>
    <tr>
      <th>411</th>
      <td>2016</td>
      <td>Benin</td>
      <td>Male</td>
      <td>87.500000</td>
      <td>2.353187</td>
      <td>2.093380</td>
      <td>2.647018</td>
    </tr>
    <tr>
      <th>412</th>
      <td>2016</td>
      <td>Benin</td>
      <td>Male</td>
      <td>92.500000</td>
      <td>2.765624</td>
      <td>2.352076</td>
      <td>3.212397</td>
    </tr>
    <tr>
      <th>413</th>
      <td>2016</td>
      <td>Benin</td>
      <td>Male</td>
      <td>110.000000</td>
      <td>3.172482</td>
      <td>2.578009</td>
      <td>3.777884</td>
    </tr>
  </tbody>
</table>
<p>414 rows × 7 columns</p>
</div>




```python
print(help(at.append_population))
```

    Help on method append_population in module __main__:

    append_population(table:pandas.core.frame.DataFrame) method of __main__.GBD_ArtifactTool instance
        Appends a new column with population data based on a rows location,
            on age, sex and year.

        Parameters
        ----------
        table:
            A pandas DataFrame that contains "age", "sex" and "year" columns

        Returns
        -------
        table with a column named population appended to it.

    None



```python
table
```


```python
del(at)
```

## 4) BFPArtifact Metrics:
- `population_for_year_with_age_limit(self, year=2016, lower=0, upper=5)`
- `population_for_year(self, year=2016)`
- `deaths_for_year_with_age_limit(self, year=2016, lower=0, upper=5)`
- `deaths_for_year(self, year =2016)`
- `live_births_for_year(self, year=2016)`
- `crude_birth_rate_for_year(self, year=2016)`
- `child_mortality_rate_for_year(self, year=2016)`
- `exposure_rates_by_year_with_age_limit(self, risk_factor, year=2016, lower=0, upper=5)`
- `relative_risk_by_year_with_age_limit(self, risk_factor, year=2016, lower=0, upper=5)`
- `SEV_for_year_with_age_limit(self, risk_factor, year=2016, lower=0, upper=5)`
- `PAF_for_year_with_age_limit(self, cause, year=2016, lower=0, upper=5)`
- `CSMR_for_year_with_age_limit(self, cause, year=2016, lower=0, upper=5)`
- `incidence_for_year_with_age_limit(self, cause, year=2016, lower=0, upper=5)`

Many of the previous methods require a `cause` or `risk_factor`. Causes and risks can have their own namespaces and are accessed using dot notation.


```python
%run /homes/dingelsz/projects/artifact_tool/bfp_artifact_tool.py
```


    <Figure size 432x288 with 0 Axes>



```python
at = BFP_ArtifactTool('/share/scratch/users/abie/bfp_2.hdf')
```


```python
at.location
```




    'Benin'




```python
at.covariates.ldi_income_per_capita()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>model_version_id</th>
      <th>covariate_id</th>
      <th>covariate_name_short</th>
      <th>location_id</th>
      <th>location_name</th>
      <th>year_id</th>
      <th>age_group_id</th>
      <th>age_group_name</th>
      <th>sex_id</th>
      <th>mean_value</th>
      <th>lower_value</th>
      <th>upper_value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1950</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1421.241577</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>1</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1951</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1411.725708</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>2</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1952</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1401.770142</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>3</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1953</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1381.191284</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>4</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1954</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1372.482422</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>5</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1955</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1362.295410</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>6</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1956</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1350.799927</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>7</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1957</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1337.985596</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>8</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1958</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1331.504395</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>9</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1959</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1330.009277</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>10</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1960</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1336.568481</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>11</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1961</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1344.550659</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>12</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1962</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1341.008179</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>13</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1963</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1344.562988</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>14</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1964</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1356.927734</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>15</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1965</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1378.101440</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>16</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1966</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1399.377197</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>17</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1967</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1418.208740</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>18</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1968</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1444.185059</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>19</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1969</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1469.006592</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>20</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1970</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1498.877075</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>21</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1971</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1523.760498</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>22</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1972</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1551.396973</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>23</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1973</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1581.484253</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>24</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1974</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1603.465942</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>25</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1975</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1592.903076</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>26</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1976</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1583.734863</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>27</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1977</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1569.399658</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>28</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1978</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1555.081909</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>29</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1979</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1551.874512</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>37</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1987</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1522.364380</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>38</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1988</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1496.577637</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>39</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1989</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1456.435669</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>40</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1990</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1428.072754</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>41</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1991</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1407.230591</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>42</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1992</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1390.824219</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>43</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1993</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1382.022217</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>44</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1994</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1362.194458</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>45</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1995</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1355.629761</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>46</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1996</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1358.634888</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>47</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1997</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1371.801270</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>48</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1998</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1387.832764</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>49</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>1999</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1411.558594</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>50</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>2000</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1442.236328</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>51</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>2001</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1476.026001</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>52</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>2002</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1514.234375</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>53</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>2003</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1551.081909</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>54</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>2004</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1589.499878</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>55</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>2005</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1618.117676</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>56</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>2006</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1641.370605</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>57</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>2007</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1665.529419</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>58</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>2008</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1690.196533</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>59</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>2009</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1707.345215</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>60</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>2010</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1715.591675</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>61</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>2011</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1720.140747</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>62</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>2012</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1729.269897</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>63</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>2013</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1749.078613</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>64</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>2014</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1779.950806</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>65</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>2015</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1816.642700</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>66</th>
      <td>18257</td>
      <td>57</td>
      <td>LDI_pc</td>
      <td>200</td>
      <td>Benin</td>
      <td>2016</td>
      <td>22</td>
      <td>All Ages</td>
      <td>3</td>
      <td>1856.089599</td>
      <td>None</td>
      <td>None</td>
    </tr>
  </tbody>
</table>
<p>67 rows × 12 columns</p>
</div>
