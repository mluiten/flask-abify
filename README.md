Current status
===
Non-functional - Not ready for production

Usage
---

1,2,3. Should be as easy as:

    {% abify('my_first_test', 'Start now! 30 days free', 'Buy now!') %}
        <a href="buy.html">{{ split_label }}</a>
    {% endabify %}

in the abify block, the following variables will be set:

* split_label
* split_key
* split_experiment
