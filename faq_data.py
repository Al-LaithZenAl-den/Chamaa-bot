# -*- coding: utf-8 -*-
"""
faq_data.py
شركة الشمعة للملكية الفكرية - بيانات البوت (شجرة الأسئلة والأجوبة)

شرح الحقول المستخدمة بكل node:
    title           : عنوان القائمة / السؤال  -> الآن dict {"ar":.., "en":..}
    staff           : اسم الموظف المسؤول عن هالقسم (اختياري) - غير معروض بالبوت حالياً
    text            : النص يلي بينعرض للمستخدم -> الآن dict {"ar":.., "en":..}
    mode            : "menu" = فيها خيارات فرعية (children) | "info" = جواب نهائي (ورقة اخيرة بالمسار)
    children        : dict فيها القوائم الفرعية { key : node }
    contacts        : list فيها جهات التواصل الخاصة بهالقسم [{"name": {"ar":..,"en":..}, "phone":..}]
    file            : اسم الملف يلي بينبعت للمستخدم عند الضغط على زر التحميل (يبقى كما هو، ما بينترجم لأنه اسم ملف فعلي على القرص)
    redirect        : مسار (path بصيغة dotted key من TREE) لقائمة تانية يتم القفز إليها مباشرة
    general_contact : True -> لعرض زر "التواصل معنا" العام (موجود بس بجذر الشجرة root)

ملاحظة: كل title/text/contact-name أصبح dict فيه "ar" و "en" حتى تشتغل دالة t() الموجودة
بـ bot.py وتعرض اللغة الصحيحة حسب اختيار المستخدم. أي محتوى جديد لازم يُضاف بنفس الشكل
{"ar": "...", "en": "..."} حتى ما يرجع يصير في خلط لغات.

ملاحظة 2: "categories_file" (تحميل ملف الفئات) لسا placeholder -> "تصنيف نيس.xlsx"
لحد ما ترفع الملف الفعلي وتعطيني اسمه الصحيح.
"""

TREE = {
    "root": {
        "title": {"ar": "القائمة الرئيسية", "en": "Main Menu"},
        "text": {
            "ar": (
                "أهلا وسهلا بكم في شركة الشمعة للملكية الفكرية.\n\n"
                "لكي نكون شركائكم في النجاح وحماية حقوقكم التجارية والفكرية، نقدم لكم:"
            ),
            "en": (
                "Welcome to Chamaa Intellectual Property Company.\n\n"
                "To be your partners in success and in protecting your commercial and "
                "intellectual property rights, we offer you:"
            ),
        },
        "mode": "menu",
        "general_contact": True,
        "children": {

            # =========================================================
            # 1) العلامات التجارية (السيد وافي)
            # =========================================================
            "trademarks": {
                "title": {"ar": "1. العلامات التجارية", "en": "1. Trademarks"},
                "staff": "السيد وافي",
                "text": {
                    "ar": "حماية العلامة التجارية يحمي منتجك من التقليد.",
                    "en": "Protecting your trademark protects your product from imitation.",
                },
                "mode": "menu",
                "contacts": [{"name": {"ar": "قسم العلامات", "en": "Trademarks Department"}, "phone": "+963 983918824"}],
                "children": {

                    "register_syria": {
                        "title": {"ar": "1.1 تسجيل علامة تجارية في سوريا", "en": "1.1 Registering a Trademark in Syria"},
                        "text": {
                            "ar": "ما هو سؤالك الذي يخص تسجيل علامة فارقة؟",
                            "en": "What is your question about trademark registration?",
                        },
                        "mode": "sequential",
                        "contacts": [{"name": {"ar": "قسم العلامات", "en": "Trademarks Department"}, "phone": "+963 983918824"}],
                        "children": {

                            "steps": {
                                "title": {"ar": "الخطوات لإنجاز العمل", "en": "Steps to Complete the Process"},
                                "text": {
                                    "ar": (
                                        "I. اختيار العلامة\n"
                                        "II. كشف مسبق للعلامة\n"
                                        "III. تقديم الأوراق وانتظار النتيجة\n"
                                        "IV. بعد القبول يتم النشر الأول في الجريدة\n"
                                        "V. النشر الثاني في الجريدة\n"
                                        "VI. استلام الشهادة"
                                    ),
                                    "en": (
                                        "I. Choosing the trademark\n"
                                        "II. Preliminary search for the trademark\n"
                                        "III. Submitting the documents and waiting for the result\n"
                                        "IV. After approval, the first publication in the official gazette\n"
                                        "V. Second publication in the official gazette\n"
                                        "VI. Receiving the certificate"
                                    ),
                                },
                                "mode": "info",
                                "contacts": [{"name": {"ar": "قسم العلامات", "en": "Trademarks Department"}, "phone": "+963 983918824"}],
                            },

                            "duration": {
                                "title": {"ar": "المدة الزمنية المتوقعة لإنجاز العمل", "en": "Expected Duration to Complete the Process"},
                                "text": {
                                    "ar": (
                                        "تتراوح المدة الإجمالية من 6 أشهر إلى 8 أشهر:\n"
                                        "- مدة القبول المبدئي: شهران تقريباً\n"
                                        "- مدة النشر الأول: 90 يوم\n"
                                        "- مدة النشر الثاني: 30 يوم\n"
                                        "- مدة استلام الشهادة: من أسبوع إلى شهرين"
                                    ),
                                    "en": (
                                        "The total duration ranges from 6 to 8 months:\n"
                                        "- Initial approval: about 2 months\n"
                                        "- First publication period: 90 days\n"
                                        "- Second publication period: 30 days\n"
                                        "- Receiving the certificate: 1 week to 2 months"
                                    ),
                                },
                                "mode": "info",
                                "contacts": [{"name": {"ar": "قسم العلامات", "en": "Trademarks Department"}, "phone": "+963 983918824"}],
                            },

                            "required_docs": {
                                "title": {"ar": "الأوراق المطلوبة", "en": "Required Documents"},
                                "text": {
                                    "ar": (
                                        "I. وكالة من قبل الكاتب بالعدل مصدقة حديثاً (3 أشهر كحد أقصى)\n"
                                        "II. سجل تجاري مصدق بنفس السنة"
                                    ),
                                    "en": (
                                        "I. A power of attorney notarized recently (no more than 3 months old)\n"
                                        "II. A commercial registry certified within the same year"
                                    ),
                                },
                                "mode": "info",
                                "contacts": [{"name": {"ar": "قسم العلامات", "en": "Trademarks Department"}, "phone": "+963 983918824"}],
                            },

                            "categories": {
                                "title": {"ar": "الفئات", "en": "Categories"},
                                "text": {
                                    "ar": (
                                        "تنقسم المواد على 45 فئة، لكل فئة موادها الخاصة "
                                        "(معلومات عن الفئات)."
                                    ),
                                    "en": (
                                        "Goods and services are divided into 45 classes, each with its own "
                                        "items (see the categories file below)."
                                    ),
                                },
                                "mode": "info",
                                "file": "تصنيف نيس.xlsx",  # TODO: استبدال بالملف الفعلي عند رفعه
                                "contacts": [{"name": {"ar": "قسم العلامات", "en": "Trademarks Department"}, "phone": "+963 983918824"}],
                            },
                        },
                    },

                    "renew_syria": {
                        "title": {"ar": "1.2 تجديد علامة تجارية في سوريا", "en": "1.2 Renewing a Trademark in Syria"},
                        "text": {
                            "ar": "ما هو سؤالك الذي يخص تجديد علامة تجارية فارقة؟",
                            "en": "What is your question about renewing a trademark?",
                        },
                        "mode": "sequential",
                        "contacts": [{"name": {"ar": "قسم العلامات", "en": "Trademarks Department"}, "phone": "+963 983918824"}],
                        "children": {

                            "steps": {
                                "title": {"ar": "الخطوات لإنجاز العمل", "en": "Steps to Complete the Process"},
                                "text": {
                                    "ar": (
                                        "I. تقديم الأوراق\n"
                                        "II. انتظار الموافقة\n"
                                        "III. استلام الشهادة"
                                    ),
                                    "en": (
                                        "I. Submitting the documents\n"
                                        "II. Waiting for approval\n"
                                        "III. Receiving the certificate"
                                    ),
                                },
                                "mode": "info",
                                "contacts": [{"name": {"ar": "قسم العلامات", "en": "Trademarks Department"}, "phone": "+963 983918824"}],
                            },

                            "required_docs": {
                                "title": {"ar": "الأوراق المطلوبة", "en": "Required Documents"},
                                "text": {
                                    "ar": (
                                        "I. وكالة من عند الكاتب بالعدل مصدقة حديثاً (3 أشهر كحد أقصى)\n"
                                        "II. سجل تجاري الذي تم تسجيل العلامة عليه سابقاً مصدق بنفس السنة\n"
                                        "(في حال تم تسجيل العلامة بدون سجل يتم تأسيس سجل جديد)"
                                    ),
                                    "en": (
                                        "I. A power of attorney notarized recently (no more than 3 months old)\n"
                                        "II. The commercial registry the trademark was originally registered under, "
                                        "certified within the same year\n"
                                        "(if the trademark was registered without a registry, a new one must be established)"
                                    ),
                                },
                                "mode": "info",
                                "contacts": [{"name": {"ar": "قسم العلامات", "en": "Trademarks Department"}, "phone": "+963 983918824"}],
                            },

                            "support": {
                                "title": {"ar": "التواصل مع الدعم", "en": "Contact Support"},
                                "text": {
                                    "ar": "يمكنكم التواصل مباشرة مع فريق الدعم لمتابعة طلبكم.",
                                    "en": "You can contact our support team directly to follow up on your request.",
                                },
                                "mode": "info",
                                "contacts": [{"name": {"ar": "قسم العلامات", "en": "Trademarks Department"}, "phone": "+963 983918824"}],
                            },
                        },
                    },

                    "abroad": {
                        "title": {
                            "ar": "1.3 تسجيل أو تجديد علامة تجارية خارج سوريا",
                            "en": "1.3 Registering or Renewing a Trademark Outside Syria",
                        },
                        "staff": "الأستاذ أحمد",
                        "text": {
                            "ar": "نقدم لكم خدمة تسجيل وحماية وتجديد العلامات التجارية في جميع دول العالم.",
                            "en": "We offer trademark registration, protection, and renewal services in all countries of the world.",
                        },
                        "mode": "info",
                        "contacts": [{"name": {"ar": "قسم العلامات الخارجية", "en": "International Trademarks Department"}, "phone": "+963 936197987"}],
                    },
                },
            },

            # =========================================================
            # 2) السجلات التجارية (دمشق-ريف دمشق) (السيد اديب النوري)
            # =========================================================
            "commercial_registry": {
                "title": {
                    "ar": "2. السجلات التجارية (دمشق - ريف دمشق)",
                    "en": "2. Commercial Registries (Damascus - Damascus Countryside)",
                },
                "staff": "السيد اديب النوري",
                "text": {
                    "ar": "يمكنك السجل التجاري من حماية علامة تجارية ويسهل عليك التعاملات التجارية.",
                    "en": "A commercial registry enables you to protect a trademark and makes commercial transactions easier for you.",
                },
                "mode": "menu",
                "contacts": [{"name": {"ar": "قسم السجلات التجارية", "en": "Commercial Registry Department"}, "phone": "+963 998100393"}],
                "children": {

                    "establish": {
                        "title": {"ar": "2.1 تأسيس سجل تجاري", "en": "2.1 Establishing a Commercial Registry"},
                        "text": {
                            "ar": "ما هو سؤالك الذي يخص السجل الفردي؟",
                            "en": "What is your question about an individual registry?",
                        },
                        "mode": "sequential",
                        "contacts": [{"name": {"ar": "قسم السجلات التجارية", "en": "Commercial Registry Department"}, "phone": "+963 998100393"}],
                        "children": {

                            "required_docs": {
                                "title": {"ar": "الأوراق المطلوبة", "en": "Required Documents"},
                                "text": {
                                    "ar": (
                                        "I. وكالة من عند الكاتب بالعدل مصدقة حديثاً (3 أشهر كحد أقصى)\n"
                                        "II. عقد تملك أو عقد إيجار لعقار تجاري أو عقد مكتب مرن\n"
                                        "III. صورة هوية / جواز سفر للأجنبي\n"
                                        "IV. صورة هوية لموظف"
                                    ),
                                    "en": (
                                        "I. A power of attorney notarized recently (no more than 3 months old)\n"
                                        "II. A property deed or lease contract for commercial premises, or a flexible office contract\n"
                                        "III. A copy of ID / passport for foreigners\n"
                                        "IV. A copy of ID for an employee"
                                    ),
                                },
                                "mode": "info",
                                "contacts": [{"name": {"ar": "قسم السجلات التجارية", "en": "Commercial Registry Department"}, "phone": "+963 998100393"}],
                            },

                            "steps": {
                                "title": {"ar": "الخطوات", "en": "Steps"},
                                "text": {
                                    "ar": (
                                        "I. تقديم الأوراق\n"
                                        "II. التوقيع والبصمة في حال عدم وجود وكالة\n"
                                        "III. الحصول على ترخيص في حال كانت الغاية بحاجة ترخيص من مؤسسة حكومية\n"
                                        "IV. تقديم نسخة موجهة لغرفة التجارة\n"
                                        "V. انتساب غرفة تجارة"
                                    ),
                                    "en": (
                                        "I. Submitting the documents\n"
                                        "II. Signature and fingerprint if no power of attorney exists\n"
                                        "III. Obtaining a license if the activity requires one from a government body\n"
                                        "IV. Submitting a copy addressed to the Chamber of Commerce\n"
                                        "V. Joining the Chamber of Commerce"
                                    ),
                                },
                                "mode": "info",
                                "contacts": [{"name": {"ar": "قسم السجلات التجارية", "en": "Commercial Registry Department"}, "phone": "+963 998100393"}],
                            },

                            "duration": {
                                "title": {"ar": "المدة الزمنية لإنجاز العمل", "en": "Time Required to Complete the Process"},
                                "text": {
                                    "ar": (
                                        "المدة الزمنية لإنجاز العمل 5 أيام دوام تقريباً، "
                                        "وذلك إذا كانت الغاية المطلوبة ليست بحاجة إلى ترخيص."
                                    ),
                                    "en": (
                                        "The process takes approximately 5 working days, "
                                        "provided the activity does not require a license."
                                    ),
                                },
                                "mode": "info",
                                "contacts": [{"name": {"ar": "قسم السجلات التجارية", "en": "Commercial Registry Department"}, "phone": "+963 998100393"}],
                            },

                            "establish_company_registry": {
                                "title": {"ar": "تأسيس سجل شركة", "en": "Establishing a Company Registry"},
                                "text": {
                                    "ar": "سيتم تحويلك إلى قائمة تأسيس شركة.",
                                    "en": "You will be redirected to the company formation menu.",
                                },
                                "mode": "info",
                                "redirect": "company_formation",
                            },
                        },
                    },

                    "renew": {
                        "title": {"ar": "2.2 تجديد سجل تجاري", "en": "2.2 Renewing a Commercial Registry"},
                        "text": {
                            "ar": "ما هو نوع السجل؟",
                            "en": "What type of registry is it?",
                        },
                        "mode": "menu",
                        "contacts": [{"name": {"ar": "قسم السجلات التجارية", "en": "Commercial Registry Department"}, "phone": "+963 998100393"}],
                        "children": {

                            "company_registry": {
                                "title": {"ar": "سجل شركة", "en": "Company Registry"},
                                "text": {
                                    "ar": "كيف يمكنني مساعدتك؟",
                                    "en": "How can I help you?",
                                },
                                "mode": "sequential",
                                "contacts": [{"name": {"ar": "قسم السجلات التجارية", "en": "Commercial Registry Department"}, "phone": "+963 998100393"}],
                                "children": {
                                    "required_docs": {
                                        "title": {"ar": "الأوراق المطلوبة", "en": "Required Documents"},
                                        "text": {
                                            "ar": (
                                                "I. وكالة من عند الكاتب بالعدل مصدقة حديثاً (3 أشهر كحد أقصى)\n"
                                                "II. عقد تملك أو عقد إيجار لعقار تجاري\n"
                                                "III. صورة هوية"
                                            ),
                                            "en": (
                                                "I. A power of attorney notarized recently (no more than 3 months old)\n"
                                                "II. A property deed or lease contract for commercial premises\n"
                                                "III. A copy of ID"
                                            ),
                                        },
                                        "mode": "info",
                                        "contacts": [{"name": {"ar": "قسم السجلات التجارية", "en": "Commercial Registry Department"}, "phone": "+963 998100393"}],
                                    },
                                    "steps": {
                                        "title": {"ar": "الخطوات", "en": "Steps"},
                                        "text": {
                                            "ar": (
                                                "I. تقديم الأوراق\n"
                                                "II. التوقيع والبصمة في حال عدم وجود وكالة\n"
                                                "III. الحصول على ترخيص في حال كانت الغاية بحاجة ترخيص من مؤسسة حكومية\n"
                                                "IV. تقديم نسخة موجهة لغرفة التجارة\n"
                                                "V. انتساب غرفة تجارة"
                                            ),
                                            "en": (
                                                "I. Submitting the documents\n"
                                                "II. Signature and fingerprint if no power of attorney exists\n"
                                                "III. Obtaining a license if the activity requires one from a government body\n"
                                                "IV. Submitting a copy addressed to the Chamber of Commerce\n"
                                                "V. Joining the Chamber of Commerce"
                                            ),
                                        },
                                        "mode": "info",
                                        "contacts": [{"name": {"ar": "قسم السجلات التجارية", "en": "Commercial Registry Department"}, "phone": "+963 998100393"}],
                                    },
                                    "duration": {
                                        "title": {"ar": "المدة الزمنية لإنجاز العمل", "en": "Time Required to Complete the Process"},
                                        "text": {
                                            "ar": "المدة الزمنية لإنجاز العمل 5 أيام عمل تقريباً.",
                                            "en": "The process takes approximately 5 working days.",
                                        },
                                        "mode": "info",
                                        "contacts": [{"name": {"ar": "قسم السجلات التجارية", "en": "Commercial Registry Department"}, "phone": "+963 998100393"}],
                                    },
                                },
                            },

                            "individual_registry": {
                                "title": {"ar": "سجل فردي", "en": "Individual Registry"},
                                "text": {
                                    "ar": "كيف يمكنني مساعدتك؟",
                                    "en": "How can I help you?",
                                },
                                "mode": "sequential",
                                "contacts": [{"name": {"ar": "قسم السجلات التجارية", "en": "Commercial Registry Department"}, "phone": "+963 998100393"}],
                                "children": {
                                    "required_docs": {
                                        "title": {"ar": "الأوراق المطلوبة", "en": "Required Documents"},
                                        "text": {
                                            "ar": (
                                                "I. وكالة من عند الكاتب بالعدل مصدقة حديثاً (3 أشهر كحد أقصى)\n"
                                                "II. عقد تملك أو عقد إيجار لعقار تجاري أو عقد مكتب مرن\n"
                                                "III. صورة هوية / جواز سفر للأجنبي"
                                            ),
                                            "en": (
                                                "I. A power of attorney notarized recently (no more than 3 months old)\n"
                                                "II. A property deed or lease contract for commercial premises, or a flexible office contract\n"
                                                "III. A copy of ID / passport for foreigners"
                                            ),
                                        },
                                        "mode": "info",
                                        "contacts": [{"name": {"ar": "قسم السجلات التجارية", "en": "Commercial Registry Department"}, "phone": "+963 998100393"}],
                                    },
                                    "steps": {
                                        "title": {"ar": "الخطوات", "en": "Steps"},
                                        "text": {
                                            "ar": (
                                                "I. تقديم الأوراق\n"
                                                "II. التوقيع والبصمة في حال عدم وجود وكالة\n"
                                                "III. الحصول على ترخيص في حال كانت الغاية بحاجة ترخيص من مؤسسة حكومية\n"
                                                "IV. تقديم نسخة موجهة لغرفة التجارة\n"
                                                "V. انتساب غرفة تجارة"
                                            ),
                                            "en": (
                                                "I. Submitting the documents\n"
                                                "II. Signature and fingerprint if no power of attorney exists\n"
                                                "III. Obtaining a license if the activity requires one from a government body\n"
                                                "IV. Submitting a copy addressed to the Chamber of Commerce\n"
                                                "V. Joining the Chamber of Commerce"
                                            ),
                                        },
                                        "mode": "info",
                                        "contacts": [{"name": {"ar": "قسم السجلات التجارية", "en": "Commercial Registry Department"}, "phone": "+963 998100393"}],
                                    },
                                    "duration": {
                                        "title": {"ar": "المدة الزمنية لإنجاز العمل", "en": "Time Required to Complete the Process"},
                                        "text": {
                                            "ar": "المدة الزمنية لإنجاز العمل 5 أيام عمل تقريباً.",
                                            "en": "The process takes approximately 5 working days.",
                                        },
                                        "mode": "info",
                                        "contacts": [{"name": {"ar": "قسم السجلات التجارية", "en": "Commercial Registry Department"}, "phone": "+963 998100393"}],
                                    },
                                },
                            },
                        },
                    },
                },
            },

            # =========================================================
            # 3) تأسيس شركة (دمشق-ريف دمشق) (السيد اديب النوري)
            # =========================================================
            "company_formation": {
                "title": {
                    "ar": "3. تأسيس شركة (دمشق - ريف دمشق)",
                    "en": "3. Company Formation (Damascus - Damascus Countryside)",
                },
                "staff": "السيد اديب النوري",
                "text": {
                    "ar": "لتأسيس شركة يجب اختيار النوع الأنسب لتجارتك.",
                    "en": "To form a company, you need to choose the type that best suits your business.",
                },
                "mode": "menu",
                "contacts": [{"name": {"ar": "قسم الشركات", "en": "Companies Department"}, "phone": "+963 998100393"}],
                "children": {

                    "llc": {
                        "title": {"ar": "شركة محدودة المسؤولية", "en": "Limited Liability Company"},
                        "text": {
                            "ar": "يوجد نوعان لشركات محدودة المسؤولية.",
                            "en": "There are two types of limited liability companies.",
                        },
                        "mode": "menu",
                        "contacts": [{"name": {"ar": "قسم الشركات", "en": "Companies Department"}, "phone": "+963 998100393"}],
                        "children": {
                            "single_member": {
                                "title": {
                                    "ar": "شركة محدودة المسؤولية شخص واحد",
                                    "en": "Single-Member Limited Liability Company",
                                },
                                "text": {
                                    "ar": (
                                        "الأكثر شيوعاً في سوريا، خاصة للمشاريع الصغيرة والمتوسطة.\n"
                                        "- شركة شخص واحد\n"
                                        "- المسؤولية: محدودة بحصة رأس المال\n"
                                        "- رأس المال: يُحدد (يتطلب إيداع مبلغ 50,000 ل.س جديدة في البنك)\n"
                                        "- لا تناسب أعمال التأمين أو المصارف\n"
                                        "- لا يمكن لغير السوري"
                                    ),
                                    "en": (
                                        "The most common type in Syria, especially for small and medium businesses.\n"
                                        "- A single-owner company\n"
                                        "- Liability: limited to the capital share\n"
                                        "- Capital: to be determined (requires depositing 50,000 new SYP in the bank)\n"
                                        "- Not suitable for insurance or banking activities\n"
                                        "- Not available to non-Syrians"
                                    ),
                                },
                                "mode": "info",
                                # الأوراق المطلوبة لهالنوع مش موجودة بالمستند الأصلي - TODO: تعبئتها
                                "contacts": [{"name": {"ar": "قسم الشركات", "en": "Companies Department"}, "phone": "+963 998100393"}],
                            },
                            "multi_member": {
                                "title": {
                                    "ar": "شركة محدودة المسؤولية عدة أشخاص",
                                    "en": "Multi-Member Limited Liability Company",
                                },
                                "text": {
                                    "ar": (
                                        "الأكثر شيوعاً في سوريا، خاصة للمشاريع الصغيرة والمتوسطة.\n"
                                        "- عدد الشركاء: من 2 إلى 50\n"
                                        "- المسؤولية: محدودة بحصة كل شريك في رأس المال\n"
                                        "- رأس المال: يُحدد (يتطلب إيداع مبلغ 50,000 ل.س جديدة في البنك)\n"
                                        "- لا تناسب أعمال التأمين أو المصارف"
                                    ),
                                    "en": (
                                        "The most common type in Syria, especially for small and medium businesses.\n"
                                        "- Number of partners: 2 to 50\n"
                                        "- Liability: limited to each partner's share of the capital\n"
                                        "- Capital: to be determined (requires depositing 50,000 new SYP in the bank)\n"
                                        "- Not suitable for insurance or banking activities"
                                    ),
                                },
                                "mode": "info",
                                # TODO: الأوراق المطلوبة غير مذكورة بالمستند الأصلي
                                "contacts": [{"name": {"ar": "قسم الشركات", "en": "Companies Department"}, "phone": "+963 998100393"}],
                            },
                        },
                    },

                    "general_partnership": {
                        "title": {"ar": "شركة تضامنية", "en": "General Partnership"},
                        "text": {
                            "ar": (
                                "تتكون من شريكين أو أكثر.\n"
                                "المسؤولية: الشركاء مسؤولون شخصياً بجميع أموالهم عن ديون الشركة.\n"
                                "تناسب الشركات الصغيرة التي تعتمد على الثقة الشخصية بين الشركاء.\n"
                                "يكتسب الشركاء صفة التاجر."
                            ),
                            "en": (
                                "Consists of two or more partners.\n"
                                "Liability: partners are personally liable with all their assets for the company's debts.\n"
                                "Suitable for small companies that rely on personal trust between partners.\n"
                                "Partners acquire the status of merchant."
                            ),
                        },
                        "mode": "info",
                        # TODO: الأوراق المطلوبة غير مذكورة بالمستند الأصلي
                        "contacts": [{"name": {"ar": "قسم الشركات", "en": "Companies Department"}, "phone": "+963 998100393"}],
                    },

                    "limited_partnership": {
                        "title": {"ar": "شركة توصية", "en": "Limited Partnership"},
                        "text": {
                            "ar": (
                                "تتكون من شركاء متضامنين (مسؤولية غير محدودة ويشاركون في الإدارة) "
                                "وشركاء موصين (مسؤولية محدودة بحصتهم في رأس المال).\n"
                                "لا يُدرج اسم الشريك الموصي في عنوان الشركة عادةً."
                            ),
                            "en": (
                                "Consists of general partners (unlimited liability, involved in management) "
                                "and limited partners (liability limited to their share of the capital).\n"
                                "A limited partner's name is usually not included in the company name."
                            ),
                        },
                        "mode": "info",
                        # TODO: الأوراق المطلوبة غير مذكورة بالمستند الأصلي
                        "contacts": [{"name": {"ar": "قسم الشركات", "en": "Companies Department"}, "phone": "+963 998100393"}],
                    },

                    "joint_stock": {
                        "title": {"ar": "شركة مساهمة", "en": "Joint-Stock Company"},
                        "text": {
                            "ar": "يوجد نوعان لشركات المساهمة.",
                            "en": "There are two types of joint-stock companies.",
                        },
                        "mode": "menu",
                        "contacts": [{"name": {"ar": "قسم الشركات", "en": "Companies Department"}, "phone": "+963 998100393"}],
                        "children": {
                            "public": {
                                "title": {"ar": "شركة مساهمة", "en": "Public Joint-Stock Company"},
                                "text": {
                                    "ar": (
                                        "عدد المساهمين 10 أشخاص على الأقل.\n"
                                        "أسهمها قابلة للتداول العام والإدراج في سوق دمشق للأوراق المالية.\n"
                                        "مناسبة للمشاريع الكبيرة."
                                    ),
                                    "en": (
                                        "At least 10 shareholders.\n"
                                        "Its shares are publicly tradable and can be listed on the Damascus Securities Exchange.\n"
                                        "Suitable for large projects."
                                    ),
                                },
                                "mode": "info",
                                # TODO: الأوراق المطلوبة غير مذكورة بالمستند الأصلي
                                "contacts": [{"name": {"ar": "قسم الشركات", "en": "Companies Department"}, "phone": "+963 998100393"}],
                            },
                            "blind": {
                                "title": {"ar": "شركة مساهمة مغفلة", "en": "Anonymous Joint-Stock Company"},
                                "text": {
                                    "ar": (
                                        "عدد المساهمين: 3 على الأقل.\n"
                                        "وتكون الدولة مساهمة بها.\n"
                                        "تخضع لأحكام خاصة."
                                    ),
                                    "en": (
                                        "At least 3 shareholders.\n"
                                        "The state is one of the shareholders.\n"
                                        "Subject to special regulations."
                                    ),
                                },
                                "mode": "info",
                                # TODO: الأوراق المطلوبة غير مذكورة بالمستند الأصلي
                                "contacts": [{"name": {"ar": "قسم الشركات", "en": "Companies Department"}, "phone": "+963 998100393"}],
                            },
                        },
                    },

                    "holding": {
                        "title": {"ar": "شركة قابضة", "en": "Holding Company"},
                        "text": {
                            "ar": (
                                "غايتها الرئيسية: تملك أسهم وحصص في شركات أخرى وإدارتها "
                                "دون ممارسة نشاط تجاري مباشر."
                            ),
                            "en": (
                                "Its main purpose: owning and managing shares and stakes in other "
                                "companies without engaging directly in commercial activity."
                            ),
                        },
                        "mode": "info",
                        # TODO: الأوراق المطلوبة غير مذكورة بالمستند الأصلي
                        "contacts": [{"name": {"ar": "قسم الشركات", "en": "Companies Department"}, "phone": "+963 998100393"}],
                    },
                },
            },

            # =========================================================
            # 4) خدمات قانونية (السيد محمد العبد الله)
            # =========================================================
            "legal_services": {
                "title": {"ar": "4. خدمات قانونية", "en": "4. Legal Services"},
                "staff": "السيد محمد العبد الله",
                "text": {
                    "ar": "اختر نوع الدعوى التي تحتاجها.",
                    "en": "Choose the type of lawsuit you need.",
                },
                "mode": "menu",
                "contacts": [{"name": {"ar": "قسم الخدمات القانونية", "en": "Legal Services Department"}, "phone": "+963 938171763"}],
                "children": {

                    "infringement_lawsuit": {
                        "title": {"ar": "دعوى تقليد", "en": "Infringement Lawsuit"},
                        "text": {
                            "ar": (
                                "تختص هذه الدعوى بالعلامات المسجلة، ويقوم أحد غير صاحب العلامة "
                                "بإنتاج أو توزيع أو بيع منتجات لنفس العلامة المحمية على هذه المنتجات، "
                                "فنقوم برفع دعوى تقليد عن طريق النيابة العامة ومديرية حماية التجارة "
                                "والصناعة، وتتم متابعة الدعوى أمام محاكم بداية الجزاء.\n\n"
                                "الأوراق المطلوبة: وكالة قضائية"
                            ),
                            "en": (
                                "This lawsuit concerns registered trademarks, where someone other than "
                                "the trademark owner produces, distributes, or sells products bearing the "
                                "same protected trademark. We file an infringement lawsuit through the "
                                "Public Prosecution and the Directorate of Trade and Industry Protection, "
                                "and the case is followed up before the criminal court of first instance.\n\n"
                                "Required documents: judicial power of attorney"
                            ),
                        },
                        "mode": "info",
                        "contacts": [
                            {"name": {"ar": "قسم المتابعات القانونية", "en": "Legal Follow-up Department"}, "phone": None},
                            {"name": {"ar": "قسم الخدمات القانونية", "en": "Legal Services Department"}, "phone": "+963 938171763"},
                        ],
                    },

                    "opposition_lawsuit": {
                        "title": {"ar": "اعتراض على علامة منشورة", "en": "Opposition to a Published Trademark"},
                        "text": {
                            "ar": (
                                "تخص هذه الدعوى الاعتراض على علامة موافق عليها من قبل المديرية "
                                "ومنشورة في جريدة الحماية خلال فترة الاعتراض (3 أشهر) من تاريخ النشر. "
                                "يصدر قرار اللجنة، وهذا القرار قابل للاعتراض عليه أمام لجنة القاضي في "
                                "حال تم رد الاعتراض على النشر، وعند صدور قرار لجنة القاضي أيضاً برد "
                                "الاعتراض يصبح قرارها قابلاً للطعن أمام محكمة البداية العامة، أي يمكن "
                                "أن يتكون الاعتراض من مرحلة واحدة أو ثلاث مراحل.\n\n"
                                "الأوراق المطلوبة: وكالة قضائية"
                            ),
                            "en": (
                                "This concerns objecting to a trademark approved by the Directorate and "
                                "published in the protection gazette, within the 3-month objection period "
                                "from the publication date. A committee decision is issued, which can be "
                                "appealed before the judge's committee if the objection is rejected; if "
                                "the judge's committee also rejects the objection, its decision can be "
                                "appealed before the general court of first instance. The objection process "
                                "may therefore involve one to three stages.\n\n"
                                "Required documents: judicial power of attorney"
                            ),
                        },
                        "mode": "info",
                        "contacts": [
                            {"name": {"ar": "قسم المتابعات القانونية", "en": "Legal Follow-up Department"}, "phone": None},
                            {"name": {"ar": "قسم الخدمات القانونية", "en": "Legal Services Department"}, "phone": "+963 938171763"},
                        ],
                    },

                    "cancellation_lawsuit": {
                        "title": {"ar": "دعوى شطب علامة", "en": "Trademark Cancellation Lawsuit"},
                        "text": {
                            "ar": (
                                "هذه الدعوى تخص علامة مسجلة للغير، ويقوم المتضرر (ذو مصلحة) بطلب "
                                "شطب لأسباب مبررة مثل (أسبقية استعمال) أو شبيهة لعلامة تخص الغير ويمكن "
                                "أن تؤدي إلى ضرر وتضليل المستهلك، فنقوم برفع دعوى شطب للعلامة مبررين "
                                "طلبه أمام محكمة البداية العامة، وتكون الدعوى خلال مدة خمس سنوات من "
                                "تاريخ تسجيلها، أما إذا ثبت سوء نية يمكن إقامة هذه الدعوى بعد مرور "
                                "هذه المدة أو خلالها (لا يوجد تقيد بالمدة).\n\n"
                                "الأوراق المطلوبة: وكالة قضائية"
                            ),
                            "en": (
                                "This lawsuit concerns a trademark registered to a third party. An "
                                "interested party who is harmed requests cancellation for justified reasons "
                                "such as prior use, or similarity to a third party's trademark that may "
                                "cause harm or mislead consumers. We file a cancellation lawsuit before the "
                                "general court of first instance, justifying the request. The lawsuit must "
                                "be filed within five years of the registration date; however, if bad faith "
                                "is proven, the lawsuit can be filed after or within this period with no "
                                "time restriction.\n\n"
                                "Required documents: judicial power of attorney"
                            ),
                        },
                        "mode": "info",
                        "contacts": [
                            {"name": {"ar": "قسم المتابعات القانونية", "en": "Legal Follow-up Department"}, "phone": None},
                            {"name": {"ar": "قسم الخدمات القانونية", "en": "Legal Services Department"}, "phone": "+963 938171763"},
                        ],
                    },

                    "appeal_lawsuit": {
                        "title": {"ar": "دعوى تظلم", "en": "Appeal Lawsuit"},
                        "text": {
                            "ar": (
                                "هذه الدعوى تخص طالب تسجيل لعلامة تم رفضها من قبل مديرية الحماية، "
                                "وقام بالاعتراض عليها أمام اللجنة المختصة وتم رد اعتراضه، حيث نقوم "
                                "برفع دعوى طعن بالقرار الصادر عن المديرية أو قرار اللجنة، وتظلمه من "
                                "هذا القرار لأحقيته بالعلامة المطلوبة.\n\n"
                                "الأوراق المطلوبة: وكالة قضائية"
                            ),
                            "en": (
                                "This lawsuit concerns an applicant whose trademark registration was "
                                "rejected by the Protection Directorate, and whose objection before the "
                                "relevant committee was also rejected. We file an appeal against the "
                                "decision issued by the Directorate or the committee, contesting the "
                                "decision on the grounds of the applicant's right to the requested "
                                "trademark.\n\n"
                                "Required documents: judicial power of attorney"
                            ),
                        },
                        "mode": "info",
                        "contacts": [
                            {"name": {"ar": "قسم المتابعات القانونية", "en": "Legal Follow-up Department"}, "phone": None},
                            {"name": {"ar": "قسم الخدمات القانونية", "en": "Legal Services Department"}, "phone": "+963 938171763"},
                        ],
                    },
                },
            },

            # =========================================================
            # 5) الحسابات
            # =========================================================
            "accounts": {
                "title": {"ar": "5. الحسابات", "en": "5. Accounts"},
                "text": {
                    "ar": "ما هو طلبك؟",
                    "en": "What is your request?",
                },
                "mode": "menu",
                "children": {

                    "account_statement": {
                        "title": {"ar": "كشف حساب", "en": "Account Statement"},
                        "text": {
                            "ar": "للحصول على كشف حساب لشركة أو لعميل يرجى التواصل مع قسم المحاسبة.",
                            "en": "To obtain an account statement for a company or a client, please contact the Accounting Department.",
                        },
                        "mode": "info",
                        "contacts": [
                            {"name": {"ar": "قسم المحاسبة", "en": "Accounting Department"}, "phone": None},
                            {"name": {"ar": "قسم الخدمات القانونية", "en": "Legal Services Department"}, "phone": "+963 938171763"},
                        ],
                    },

                    "cost_inquiry": {
                        "title": {"ar": "الاستفسار عن تكلفة", "en": "Cost Inquiry"},
                        "text": {
                            "ar": "لمعلومات عن تكلفة الخدمات يمكنك التواصل مع قسم المحاسبة.",
                            "en": "For information about service costs, you can contact the Accounting Department.",
                        },
                        "mode": "info",
                        "contacts": [{"name": {"ar": "قسم المحاسبة", "en": "Accounting Department"}, "phone": None}],
                    },
                },
            },

            # =========================================================
            # 6) طلبات مستقلة (السيد وافي)
            # =========================================================
            "independent_requests": {
                "title": {"ar": "6. طلبات مستقلة", "en": "6. Independent Requests"},
                "staff": "السيد وافي",
                "text": {
                    "ar": "ما هو طلبك؟",
                    "en": "What is your request?",
                },
                "mode": "menu",
                "contacts": [{"name": {"ar": "قسم الطلبات", "en": "Requests Department"}, "phone": "+963 983918824"}],
                "children": {

                    "customs_circular": {
                        "title": {"ar": "تعميم جمارك", "en": "Customs Circular"},
                        "text": {
                            "ar": (
                                "في حال قيام أحد الأشخاص بإدخال بضائع من المنافذ الحدودية تحمل "
                                "العلامة التجارية التي تمتلكها، يمكنك منع إدخالها من خلال تعميم "
                                "الجمارك.\n\n"
                                "الأوراق المطلوبة: وكالة فقط، أو وكالة + سجل تجاري للشركات"
                            ),
                            "en": (
                                "If someone brings goods across a border crossing bearing your "
                                "trademark, you can prevent their entry through a customs circular.\n\n"
                                "Required documents: power of attorney only, or power of attorney + "
                                "commercial registry for companies"
                            ),
                        },
                        "mode": "info",
                        "contacts": [
                            {"name": {"ar": "قسم متابعة المعاملات", "en": "Transactions Follow-up Department"}, "phone": None},
                            {"name": {"ar": "قسم الطلبات", "en": "Requests Department"}, "phone": "+963 983918824"},
                        ],
                    },

                    "certified_copy": {
                        "title": {"ar": "صورة طبق الأصل", "en": "Certified True Copy"},
                        "text": {
                            "ar": (
                                "صورة طبق الأصل عن (شهادة علامة فارقة - قرار محكمة - قرار لجنة "
                                "القاضي - شهادة الوقوعة).\n\n"
                                "الأوراق المطلوبة: وكالة فقط"
                            ),
                            "en": (
                                "A certified true copy of (a trademark certificate - a court ruling - "
                                "a judge's committee decision - an incident certificate).\n\n"
                                "Required documents: power of attorney only"
                            ),
                        },
                        "mode": "info",
                        "contacts": [
                            {"name": {"ar": "قسم متابعة المعاملات", "en": "Transactions Follow-up Department"}, "phone": None},
                            {"name": {"ar": "قسم الطلبات", "en": "Requests Department"}, "phone": "+963 983918824"},
                        ],
                    },

                    "prior_search": {
                        "title": {"ar": "كشف مسبق عن علامة", "en": "Preliminary Trademark Search"},
                        "text": {
                            "ar": "إذا كنت ترغب في الحصول على كشف مسبق مع دراسة إمكانية قبول العلامة المطلوبة.",
                            "en": "If you would like a preliminary search along with an assessment of the likelihood of the trademark being accepted.",
                        },
                        "mode": "info",
                        "contacts": [
                            {"name": {"ar": "قسم متابعة المعاملات", "en": "Transactions Follow-up Department"}, "phone": None},
                            {"name": {"ar": "قسم الطلبات", "en": "Requests Department"}, "phone": "+963 983918824"},
                        ],
                    },
                },
            },

            # =========================================================
            # 7) نموذج أو رسم صناعي (السيد محمد العبد الله)
            # =========================================================
            "industrial_design": {
                "title": {"ar": "7. نموذج أو رسم صناعي", "en": "7. Industrial Model or Design"},
                "staff": "السيد محمد العبد الله",
                "text": {
                    "ar": (
                        "لحماية نموذج أو رسم صناعي يمكنك التواصل مع قسم الحماية.\n\n"
                        "الأوراق المطلوبة: وكالة + سجل تجاري + صورة النموذج أو الرسم"
                    ),
                    "en": (
                        "To protect an industrial model or design, you can contact the Protection "
                        "Department.\n\n"
                        "Required documents: power of attorney + commercial registry + an image of "
                        "the model or design"
                    ),
                },
                "mode": "info",
                "contacts": [
                    {"name": {"ar": "قسم الحماية", "en": "Protection Department"}, "phone": None},
                    {"name": {"ar": "قسم حماية الملكية", "en": "IP Protection Department"}, "phone": "+963 938171763"},
                ],
            },

            # =========================================================
            # 8) الحماية الفكرية (السيد محمد العبد الله)
            # =========================================================
            "intellectual_protection": {
                "title": {"ar": "8. الحماية الفكرية", "en": "8. Intellectual Protection"},
                "staff": "السيد محمد العبد الله",
                "text": {
                    "ar": (
                        "يمكنك الاستفادة منها لحماية (كتاب - مؤلفات - مقطوعات - تطبيقات ومواقع "
                        "إلكترونية - برامج ودورات تدريبية - مسلسلات وأفلام - مطبوعات - مقالات).\n\n"
                        "الأوراق المطلوبة: وكالة + شرح تفصيلي كتابي عن المطلوب حمايته"
                    ),
                    "en": (
                        "You can use this service to protect (a book - written works - musical pieces "
                        "- apps and websites - software and training courses - series and films - "
                        "publications - articles).\n\n"
                        "Required documents: power of attorney + a detailed written description of "
                        "what needs to be protected"
                    ),
                },
                "mode": "info",
                "contacts": [
                    {"name": {"ar": "قسم الحماية الفكرية", "en": "Intellectual Protection Department"}, "phone": None},
                    {"name": {"ar": "قسم حماية الملكية", "en": "IP Protection Department"}, "phone": "+963 938171763"},
                ],
            },
        },
    },
}