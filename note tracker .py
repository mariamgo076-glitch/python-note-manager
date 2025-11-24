from datetime import datetime
import json

class Note:
    def __init__(self, note_id, title, content, tags, created_at, updated_at, note_type):
        self.note_id=note_id
        self.title=title
        self.content=content
        self.tags = tags if tags is not None else []
        self.created_at = created_at if created_at is not None else datetime.now()
        self.updated_at = updated_at if updated_at is not None else self.created_at
        self.note_type=note_type


    def update_title(self, new_title):
        """
        يحدّث عنوان النوت.
        """
        self.title=new_title
        self.updated_at=datetime.now()

    def update_content(self, new_content):
        """
        يحدّث محتوى النوت.
        """
        self.content=new_content
        self.updated_at=datetime.now()

    def update_tags(self, new_tags):
        """
        يحدّث التاجز الخاصة بالنوت.
        """
        self.tags=new_tags if new_tags is not None else []
        self.updated_at=datetime.now()
    def update_note_type(self, new_type):
        """
        يغيّر نوع النوت (Task, Idea, Bookmark...).
        """
        self.note_type=new_type
        self.updated_at=datetime.now()

    def to_dict(self):
        """
        يعيد بيانات النوت على شكل dictionary لحفظها في JSON.
        """
        return {
        "note_id": self.note_id,
        "title": self.title,
        "content": self.content,
        "tags": self.tags,
        "created_at": self.created_at.isoformat(),
        "updated_at": self.updated_at.isoformat(),
        "note_type": self.note_type
    }

    @staticmethod
    def from_dict(data):
        """
     ينشئ كائن Note من dict محمّلة من JSON.
    """
        return Note(
            note_id=data["note_id"],
            title=data["title"],
            content=data["content"],
            tags=data.get("tags", []),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            note_type=data.get("note_type", "note")
        )
class NoteManager:
    def __init__(self):
        """
        يحمل كل النوتس في ليست notes
        ويحاول تحميل البيانات من الملف JSON.
        """
        self.notes=[]
        self.load_notes()

    def load_notes(self):
        """
        يقرأ ملف JSON ويحمّل النوتس إلى الذاكرة.
        """
        try:
            with open('notes.json','r') as f:
                data=json.load(f)
                self.notes= [Note.from_dict(item) for item in data]
        except FileNotFoundError:
            self.notes=[]

    def save_notes(self):
        """
        يحفظ كل النوتس الحالية في ملف JSON.
    """
        import json

    # 1) جهّزي لست جديدة فيها النوتات في صورة dict
        new = []
        for note in self.notes:
            x = note.to_dict()
            new.append(x)

    # 2) افتحي ملف JSON واكتبي فيه الليست الجديدة
        with open("notes.json", "w", encoding="utf-8") as f:
            json.dump(new, f, indent=4, ensure_ascii=False)

    def add_note(self, note):
        """
        يضيف نوت جديدة للمدير ثم يحفظ الملف.
        """
        self.notes.append(note)
        self.save_notes()

    def delete_note(self, note_id):
        """
        يحذف نوت بناءً على ID.
        """
        for note in self.notes:
            if note.note_id == note_id:
                self.notes.remove(note)
                break
        self.save_notes()

    def get_note_by_id(self, note_id):
        for note in self.notes:
            if str(note.note_id) == str(note_id):
             return note
        return None

    def update_note(self, note_id, **kwargs):
        """
        يحدّث خصائص نوت معينة (عنوان/محتوى/تاجز...)
        """

    def search_by_title(self, keyword):
        """
        يبحث عن نوتس تحتوي العنوان بتاعها على keyword.
        """
        l=[]
        for note in self.notes:
            if keyword in note.title:
                l.append(note)
            

        return l


    def search_by_tag(self, tag):
        """
        يرجع كل النوتس اللي تحتوي على التاج المطلوب.
        """
        l=[]
        for note in self.notes:
            if tag in note.tags:
                l.append(note)
        return l
    def search_by_content(self, keyword):
        """
        يبحث داخل محتوى النوتس عن keyword.
        """
        l=[]
        for note in self.notes:
            if keyword in note.content:
                l.append(note)
        return l

    def search_by_date(self, date):
        """
        يرجع النوتس اللي اتعملت في تاريخ معيّن.
        """
        l=[]
        for note in self.notes:
            if note.created_at == date:
                l.append(note)
        return l

    def sort_by_title(self):
            """
            يرتب النوتس أبجديًا حسب العنوان.
            """
            self.notes.sort(key=lambda note: note.title)
            
    def sort_by_date(self):
        self.notes.sort(key=lambda note: note.created_at, reverse=True)
        return self.notes
       
    def sort_by_update(self):
        """
        يرتب النوتس حسب آخر تعديل.
        """
        self.notes.sort(key=lambda note: note.updated_at, reverse=True)

    def sort_by_length(self):
        """
        يرتب النوتس حسب طول المحتوى.
        """
        max(self.notes, key=lambda note: len(note.content))
    def sort_by_tags_count(self):
        """
        يرتب النوتس حسب عدد التاجز.
        """
        self.notes.sort(key=lambda note: len(note.tags), reverse=True)

def show_menu():
    print('-------- THE MAIN MENU---------')
    print('ENTER YOUR CHIOCE?')
    print('1-ADD NOTE.')
    print('2-UPDATE NOTE.')
    print('3-DELETE NOTE.')
    print('4-SEARCH.')
    print('5-SORTING.')
    print('6-EXITdefING.')


def get_user_choice():
    """
    يأخذ اختيار المستخدم من المينيو.
    """
    choice=input('ENTER YOUR CHOICE:')
    return choice

def handle_add_note(manager):
    title = input("Enter title: ")
    content = input("Enter content: ")
    tags = input("Enter tags (comma separated): ").split(",")

    note_id = len(manager.notes) + 1

    note = Note(
        note_id=note_id,
        title=title,
        content=content,
        tags=tags,
        created_at=None,
        updated_at=None,
        note_type="note"
    )

    manager.add_note(note)
    print("Note added successfully!")

def handle_edit_note(manager):
    """
    يسمح بتعديل نوت موجودة.
    """
    id=input('ENTER THE ID FOR THE WANTED NOTE:')
    if manager.get_note_by_id(id) == None:
        print('THER IS NO ID LIKE THIS!')
    else:
        note = manager.get_note_by_id(id)


    print("CURRENT TITLE:", note.title)
    print("CURRENT CONTENT:", note.content)
    print("CURRENT TAGS:", note.tags)
    print("TYPE:", note.note_type)
        

def handle_delete_note(manager):
    """
    يحذف نوت بناءً على ID.
    """
    id=input('ENTER THE ID FOR THE WANTED NOTE:')
    if manager.get_note_by_id(id) == None:
        print('THER IS NO ID LIKE THIS!')
    else:
        note=manager.get_note_by_id(id)
        manager.notes.remove(note)
        print(manager.notes)
def handle_search(manager):
    """
    يفتح قائمة بحث ويستقبل طريقة البحث (عنوان/تاج/تاريخ...).
    """
    text='''
    SEARCH!
    1-Searching by note.
    2-Searching by date.
    3-Searching by tags.
    CHOOSE :'''
    search=input(text)
    if search == '1':
        title=input('Enter the title:')
        note=manager.search_by_title(title)
        print(note)
    elif search=='2':
        date=input('ENTER THE DATE:')
        note=manager.search_by_date(date)
        print(note)
    elif search=='3':
        tag=input("ENTER THE NOTE'S TAG:")
        note=manager.search_by_tag(tag)
        print(note)
    else:
        print("you haven't that choice!")

def handle_sort(manager):
    print("""
    SORT MENU
    1- Sort by date
    2- Sort by length
    3- Sort by title
    """)

    choice = input("Choose sorting type: ")

    if choice == "1":
        sorted_notes = manager.sort_by_date()
        for note in sorted_notes:
            print(note)

    elif choice == "2":
        sorted_notes = manager.sort_by_length()
        for note in sorted_notes:
            print(note)

    elif choice == "3":
        sorted_notes = manager.sort_by_title()
        for note in sorted_notes:
            print(note)

    else:
        print("INVALID CHOICE!")

    
def main():
    manager = NoteManager()   # إنشاء مدير النوتس

    while True:               # لوب البرنامج الأساسي
        show_menu()           # نعرض المينيو للمستخدم
        choice = get_user_choice()   # ناخد اختيار المستخدم

        if choice == '1':
            handle_add_note(manager)

        elif choice == '2':
            handle_edit_note(manager)

        elif choice == '3':
            handle_delete_note(manager)

        elif choice == '4':
            handle_search(manager)

        elif choice == '5':
            handle_sort(manager)

        elif choice == '6':
            print("Exiting program...")
            break

        else:
            print("Invalid choice! Try again.")
if __name__ == "__main__":
    main()
