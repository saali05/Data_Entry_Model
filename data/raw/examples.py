EXAMPLES = [
    {
        "text": "Name: Rahul, Account: 123456789012, IFSC: SBIN0001234, Amount: ₹5000",
        "entities": {
            "NAME": "Rahul",
            "ACCOUNT_NUMBER": "123456789012",
            "IFSC_CODE": "SBIN0001234",
            "AMOUNT": "₹5000",
        },
    },
    {
        "text": "pls trf ₹7500 to Anil acc 987654321098 ifsc HDFC0001234",
        "entities": {
            "NAME": "Anil",
            "ACCOUNT_NUMBER": "987654321098",
            "IFSC_CODE": "HDFC0001234",
            "AMOUNT": "₹7500",
        },
    },
    {
        "text": "IFSC ICIC0001234, account 111122223333, send 12500 to Priya",
        "entities": {
            "NAME": "Priya",
            "ACCOUNT_NUMBER": "111122223333",
            "IFSC_CODE": "ICIC0001234",
            "AMOUNT": "12500",
        },
    },
    {
        "text": "Kumar A/C 555566667777 Amt Rs. 25000 Code SBIN0005678",
        "entities": {
            "NAME": "Kumar",
            "ACCOUNT_NUMBER": "555566667777",
            "IFSC_CODE": "SBIN0005678",
            "AMOUNT": "25000",
        },
    },
    {
        "text": "Please transfer 18000 rupees to Meera using account 222233334444 and IFSC HDFC0005678.",
        "entities": {
            "NAME": "Meera",
            "ACCOUNT_NUMBER": "222233334444",
            "IFSC_CODE": "HDFC0005678",
            "AMOUNT": "18000",
        },
    },
    {
        "text": "Transfer ₹3200 to Arun. A/c 333344445555. IFSC ICIC0004567.",
        "entities": {
            "NAME": "Arun",
            "ACCOUNT_NUMBER": "333344445555",
            "IFSC_CODE": "ICIC0004567",
            "AMOUNT": "₹3200",
        },
    },
    {
        "text": "Send Rs 4500 to Neha account 444455556666 IFSC SBIN0007890",
        "entities": {
            "NAME": "Neha",
            "ACCOUNT_NUMBER": "444455556666",
            "IFSC_CODE": "SBIN0007890",
            "AMOUNT": "Rs 4500",
        },
    },
    {
        "text": "Beneficiary: Vijay, A/C: 666677778888, Code: HDFC0003456, Amount: ₹12000",
        "entities": {
            "NAME": "Vijay",
            "ACCOUNT_NUMBER": "666677778888",
            "IFSC_CODE": "HDFC0003456",
            "AMOUNT": "₹12000",
        },
    },
    {
        "text": "pls send 8500 INR to Suresh acc no 777788889999 ifsc ICIC0006789",
        "entities": {
            "NAME": "Suresh",
            "ACCOUNT_NUMBER": "777788889999",
            "IFSC_CODE": "ICIC0006789",
            "AMOUNT": "8500 INR",
        },
    },
    {
        "text": "Account 888899990000 belongs to Divya. Transfer ₹15000. IFSC SBIN0001111.",
        "entities": {
            "NAME": "Divya",
            "ACCOUNT_NUMBER": "888899990000",
            "IFSC_CODE": "SBIN0001111",
            "AMOUNT": "₹15000",
        },
    },
    {
        "text": "Send 6000 to Ramesh, IFSC HDFC0002222, account 999900001111.",
        "entities": {
            "NAME": "Ramesh",
            "ACCOUNT_NUMBER": "999900001111",
            "IFSC_CODE": "HDFC0002222",
            "AMOUNT": "6000",
        },
    },
    {
        "text": "Priya account no 121212121212, IFSC ICIC0003333, please transfer Rs. 9500.",
        "entities": {
            "NAME": "Priya",
            "ACCOUNT_NUMBER": "121212121212",
            "IFSC_CODE": "ICIC0003333",
            "AMOUNT": "Rs. 9500",
        },
    },
    {
        "text": "Transfer 11000 to Ajay. Bank code SBIN0004444. A/C 343434343434.",
        "entities": {
            "NAME": "Ajay",
            "ACCOUNT_NUMBER": "343434343434",
            "IFSC_CODE": "SBIN0004444",
            "AMOUNT": "11000",
        },
    },
    {
        "text": "Meena / 565656565656 / HDFC0005555 / ₹7000",
        "entities": {
            "NAME": "Meena",
            "ACCOUNT_NUMBER": "565656565656",
            "IFSC_CODE": "HDFC0005555",
            "AMOUNT": "₹7000",
        },
    },
    {
        "text": "Please pay ₹13500 to Rohit. Account: 787878787878 IFSC: ICIC0006666",
        "entities": {
            "NAME": "Rohit",
            "ACCOUNT_NUMBER": "787878787878",
            "IFSC_CODE": "ICIC0006666",
            "AMOUNT": "₹13500",
        },
    },
    {
        "text": "A/C 909090909090, Rahul, SBIN0007777, send 21000",
        "entities": {
            "NAME": "Rahul",
            "ACCOUNT_NUMBER": "909090909090",
            "IFSC_CODE": "SBIN0007777",
            "AMOUNT": "21000",
        },
    },
    {
        "text": "Transfer Rs. 5500 to Kavya using account 232323232323 and IFSC HDFC0008888.",
        "entities": {
            "NAME": "Kavya",
            "ACCOUNT_NUMBER": "232323232323",
            "IFSC_CODE": "HDFC0008888",
            "AMOUNT": "Rs. 5500",
        },
    },
    {
        "text": "Kiran needs ₹16000. A/c 454545454545. IFSC ICIC0009999.",
        "entities": {
            "NAME": "Kiran",
            "ACCOUNT_NUMBER": "454545454545",
            "IFSC_CODE": "ICIC0009999",
            "AMOUNT": "₹16000",
        },
    },
    {
        "text": "Send 27500 INR to Deepak. Account 676767676767. Code SBIN0001010.",
        "entities": {
            "NAME": "Deepak",
            "ACCOUNT_NUMBER": "676767676767",
            "IFSC_CODE": "SBIN0001010",
            "AMOUNT": "27500 INR",
        },
    },
    {
        "text": "Beneficiary Anu, amount ₹4000, account 898989898989, IFSC HDFC0001212.",
        "entities": {
            "NAME": "Anu",
            "ACCOUNT_NUMBER": "898989898989",
            "IFSC_CODE": "HDFC0001212",
            "AMOUNT": "₹4000",
        },
    },
        {
        "text": "sugunan, ₹4000, 898989898989, HDFC0001212.",
        "entities": {
            "NAME": "sugunan",
            "ACCOUNT_NUMBER": "898989898989",
            "IFSC_CODE": "HDFC0001212",
            "AMOUNT": "₹4000",
        },
    },
]