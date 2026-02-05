#!/usr/bin/env python3
"""
Insert guided practice exercises into the PTX file at correct locations
"""

import re

# Define insertion points based on context (text to search for in PTX file)
# Each entry is (search_text, insert_after_match)
INSERTION_POINTS = [
    # GP1: After fig-FourCaseStudies, before "The case study for the medical consultant"
    ('</figure>', 59),  # Line 58 in PTX
    
    # GP2: After "In @fig-satActNormals" text about SAT/ACT comparison
    # Need to find the context in PTX
    ('fig-satActNormals', None),  # Will search
    
    # GP3: After Z score definition, before "Observations above the mean"
    ('Z score formula', None),
    
    # GP4: After worked example about possum, before "We can use Z scores"
    ('possum', None),
    
    # GP5: After "One observation x_1 is said to be more unusual"
    ('more unusual', None),
    
    # GP6: After Nel's percentile example
    ('Nel', None),
    
    # GP7: After Shannon scoring example
    ('Shannon', None),
    
    # GP8: After Stuart example
    ('Stuart', None),
    
    # GP9: After 82nd percentile example
    ('82', None),
    
    # GP10: After GP9, another height example
    ('male adult', None),
    
    # GP11: After between example
    ('between', None),
    
    # GP12: After GP11
    ('5\'5', None),
    
    # GP13: After 68-95-99.7 rule figure
    ('68%', None),
    
    # GP14: After 68-95-99.7 discussion
    ('rare', None),
    
    # GP15: After confidence interval introduction
    ('1.96', None),
    
    # GP16: After confidence interval figure
    ('fig-95PercentConfidenceInterval', None),
]

# The extracted GP blocks (from previous script)
GP_XMLS = [
    # GP1
    """    <exercise>
      <title>Guided Practice</title>
      <statement>
      <p>Describe the shape of the distributions and note anything that you find interesting.</p>
      </statement>
      <solution>
      <p>In general, the distributions are reasonably symmetric.</p>
      <p>The case study for the medical consultant is the only distribution with any evident skew (the distribution is skewed right).</p>
      </solution>
    </exercise>""",
    
    # GP2
    """    <exercise>
      <title>Guided Practice</title>
      <statement>
      <p>SAT scores follow a nearly normal distribution with a mean of 1500 points and a standard deviation of 300 points.</p>
      <p>ACT scores also follow a nearly normal distribution with mean of 21 points and a standard deviation of 5 points.</p>
      <p>Suppose Nel scored 1800 points on their SAT and Sian scored 24 points on their ACT.</p>
      <p>Who performed better?</p>
      </statement>
      <solution>
      <p>We use the standard deviation as a guide.</p>
      <p>Nel is 1 standard deviation above average on the SAT: <m>1500 + 300 = 1800.</m> Sian is 0.6 standard deviations above the mean on the ACT: <m>21+0.6 \\times 5 = 24.</m> In <xref ref="fig-satActNormals" />, we can see that Nel did better compared to other test takers than Sian did, so their score was better.</p>
      </solution>
    </exercise>""",
    
    # GP3
    """    <exercise>
      <title>Guided Practice</title>
      <statement>
      <p>Use Sian's ACT score, 24, along with the ACT mean and standard deviation to compute their Z score.</p>
      </statement>
      <solution>
      <p><m>Z_{Sian} = \\frac{x_{Sian} - \\mu_{ACT}}{\\sigma_{ACT}} = \\frac{24 - 21}{5} = 0.6</m></p>
      </solution>
    </exercise>""",
    
    # GP4
    """    <exercise>
      <title>Guided Practice</title>
      <statement>
      <p>Head lengths of brushtail possums follow a nearly normal distribution with mean 92.6 mm and standard deviation 3.6 mm.</p>
      <p>Compute the Z scores for possums with head lengths of 95.4 mm and 85.8 mm.</p>
      </statement>
      <solution>
      <p>For <m>x_1=95.4</m> mm: <m>Z_1 = \\frac{x_1 - \\mu}{\\sigma} = \\frac{95.4 - 92.6}{3.6} = 0.78.</m> For <m>x_2=85.8</m> mm: <m>Z_2 = \\frac{85.8 - 92.6}{3.6} = -1.89.</m></p>
      </solution>
    </exercise>""",
    
    # GP5
    """    <exercise>
      <title>Guided Practice</title>
      <statement>
      <p>Which of the two brushtail possum observations in the previous guided practice is more <em>unusual</em>?</p>
      </statement>
      <solution>
      <p>Because the <em>absolute value</em> of Z score for the second observation is larger than that of the first, the second observation has a more unusual head length.</p>
      </solution>
    </exercise>""",
    
    # GP6
    """    <exercise>
      <title>Guided Practice</title>
      <statement>
      <p>Determine the proportion of SAT test takers who scored better than Nel on the SAT.</p>
      </statement>
      <solution>
      <p>If 84% had lower scores than Nel, the number of people who had better scores must be 16%.</p>
      <p>(Generally ties are ignored when the normal model, or any other continuous distribution, is used.)</p>
      </solution>
    </exercise>""",
    
    # GP7
    """    <exercise>
      <title>Guided Practice</title>
      <statement>
      <p>If the probability of Shannon scoring at least 1630 is 0.3336, then what is the probability they score less than 1630?</p>
      <p>Draw the normal curve representing this exercise, shading the lower region instead of the upper one.</p>
      </statement>
      <solution>
      <p>We found the probability to be 0.6664.</p>
      <p>A picture for this exercise is represented by the shaded area below "0.6664".</p>
      </solution>
    </exercise>""",
    
    # GP8
    """    <exercise>
      <title>Guided Practice</title>
      <statement>
      <p>Stuart earned an SAT score of 2100.</p>
      <p>Draw a picture for each part.</p>
      <ol>
        <li><p>What is their percentile?</p></li>
        <li><p>What percent of SAT takers did better than Stuart?</p></li>
      </ol>
      </statement>
      <solution>
      <p>Numerical answers: (a) 0.9772.</p>
      <p>(b) 0.0228.</p>
      </solution>
    </exercise>""",
    
    # GP9
    """    <exercise>
      <title>Guided Practice</title>
      <statement>
      <p>Using Z scores, answer the following questions.</p>
      <ol>
        <li><p>What is the <m>95^{th}</m> percentile for SAT scores?</p></li>
        <li><p>What is the <m>97.5^{th}</m> percentile of the male heights? As always with normal probability problems, first draw a picture.</p></li>
      </ol>
      </statement>
      <solution>
      <p>Remember: draw a picture first, then find the Z score.</p>
      <p>(We leave the pictures to you.) The Z score can be found by using the percentiles and the normal probability table.</p>
      <p>(a) We look for 0.95 in the probability portion (middle part) of the normal probability table, which leads us to row 1.6 and (about) column 0.05, i.e., <m>Z_{95}=1.65.</m> Knowing <m>Z_{95}=1.65,</m> <m>\\mu = 1500,</m> and <m>\\sigma = 300,</m> we setup the Z score formula: <m>1.65 = \\frac{x_{95} - 1500}{300}.</m> We solve for <m>x_{95}</m>: <m>x_{95} = 1995.</m> (b) Similarly, we find <m>Z_{97.5} = 1.96,</m> again setup the Z score formula for the heights, and calculate <m>x_{97.5} = 76.5.</m></p>
      </solution>
    </exercise>""",
    
    # GP10
    """    <exercise>
      <title>Guided Practice</title>
      <statement>
      <p>Using Z scores, answer the following questions.</p>
      <ol>
        <li><p>What is the probability that a randomly selected male adult is at least 6'2" (74 inches)?</p></li>
        <li><p>What is the probability that a male adult is shorter than 5'9" (69 inches)?</p></li>
      </ol>
      </statement>
      <solution>
      <p>Numerical answers: (a) 0.1131.</p>
      <p>(b) 0.3821.</p>
      </solution>
    </exercise>""",
    
    # GP11
    """    <exercise>
      <title>Guided Practice</title>
      <statement>
      <p>Find the percent of SAT takers who earn between 1500 and 2000.</p>
      </statement>
      <solution>
      <p>This is an abbreviated solution.</p>
      <p>(Be sure to draw a figure!) First find the percent who get below 1500 and the percent that get above 2000: <m>Z_{1500} = 0.00 \\to 0.5000</m> (area below), <m>Z_{2000} = 1.67 \\to 0.0475</m> (area above).</p>
      <p>Final answer: <m>1.0000-0.5000 - 0.0475 = 0.4525.</m></p>
      </solution>
    </exercise>""",
    
    # GP12
    """    <exercise>
      <title>Guided Practice</title>
      <statement>
      <p>What percent of adult males are between 5'5" and 5'7"?</p>
      </statement>
      <solution>
      <p>5'5" is 65 inches.</p>
      <p>5'7" is 67 inches.</p>
      <p>Numerical solution: <m>1.000 - 0.0649 - 0.8183 = 0.1168,</m> i.e., 11.68%.</p>
      </solution>
    </exercise>""",
    
    # GP13
    """    <exercise>
      <title>Guided Practice</title>
      <statement>
      <p>Use <c>pnorm()</c> (or a Z table) to confirm that about 68%, 95%, and 99.7% of observations fall within 1, 2, and 3, standard deviations of the mean in the normal distribution, respectively.</p>
      <p>For instance, first find the area that falls between <m>Z=-1</m> and <m>Z=1,</m> which should have an area of about 0.68.</p>
      <p>Similarly there should be an area of about 0.95 between <m>Z=-2</m> and <m>Z=2.</m></p>
      </statement>
      <solution>
      <p>First draw the pictures.</p>
      <p>To find the area between <m>Z=-1</m> and <m>Z=1,</m> use <c>pnorm()</c> or the normal probability table to determine the areas below <m>Z=-1</m> and above <m>Z=1.</m> Next verify the area between <m>Z=-1</m> and <m>Z=1</m> is about 0.68.</p>
      <p>Repeat this for <m>Z=-2</m> to <m>Z=2</m> and for <m>Z=-3</m> to <m>Z=3.</m></p>
      </solution>
    </exercise>""",
    
    # GP14
    """    <exercise>
      <title>Guided Practice</title>
      <statement>
      <p>SAT scores closely follow the normal model with mean <m>\\mu = 1500</m> and standard deviation <m>\\sigma = 300.</m> About what percent of test takers score 900 to 2100?</p>
      <p>What percent score between 1500 and 2100 ?</p>
      </statement>
      <solution>
      <p>900 and 2100 represent two standard deviations above and below the mean, which means about 95% of test takers will score between 900 and 2100.</p>
      <p>Since the normal model is symmetric, then half of the test takers from part (a) (<m>\\frac{95\\%}{2} = 47.5\\%</m> of all test takers) will score 900 to 1500 while 47.5% score between 1500 and 2100.</p>
      </solution>
    </exercise>""",
    
    # GP15
    """    <exercise>
      <title>Guided Practice</title>
      <statement>
      <p>Compute the area between -1.96 and 1.96 for a normal distribution with mean 0 and standard deviation 1.</p>
      </statement>
      <solution>
      <p>We will leave it to you to draw a picture.</p>
      <p>The Z scores are <m>Z_{left} = -1.96</m> and <m>Z_{right} = 1.96.</m> The area between these two Z scores is <m>0.9750 - 0.0250 = 0.9500.</m> This is where "1.96" comes from in the 95% confidence interval formula.</p>
      </solution>
    </exercise>""",
    
    # GP16
    """    <exercise>
      <title>Guided Practice</title>
      <statement>
      <p>In <xref ref="fig-95PercentConfidenceInterval" />, one interval does not contain the true proportion, <m>p = 0.3.</m> Does this imply that there was a problem with the datasets that were selected?</p>
      </statement>
      <solution>
      <p>No.</p>
      <p>Just as some observations occur more than 1.96 standard deviations from the mean, some point estimates will be more than 1.96 standard errors from the parameter.</p>
      <p>A confidence interval only provides a plausible range of values for a parameter.</p>
      <p>While we might say other values are implausible based on the data, this does not mean they are impossible.</p>
      </solution>
    </exercise>""",
]

def main():
    print(f"Total GP exercises to insert: {len(GP_XMLS)}")
    
if __name__ == '__main__':
    main()
