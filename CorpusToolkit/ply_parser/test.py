import logging

from CorpusToolkit.ply_parser import make_parser, lexer

logging.basicConfig(
    level=logging.DEBUG,
    filename="parselog.txt",
    filemode="w",
    format="%(filename)10s:%(lineno)4d:%(message)s"
)
log = logging.getLogger()

test_data = (
    "19980101-01-001-002/m  中共中央/nt  总书记/n  、/wu  国家/n  主席/n  江/nrf  泽民/nrg",
    "19980101-01-001-006/m  在/p  １９９８年/t  来临/vi  之际/f  ，/wd  我/rr  十分/dc  高兴/a  地/ui  通过/p  [中央/n  人民/n  广播/vn  电台/n]nt  、/wu  [中国/ns  国际/n  广播/vn  电台/n]nt  和/c  [中央/n  电视台/n]nt  ，/wd  向/p  全国/n  各族/rz  人民/n  ，/wd  向/p  [香港/ns  特别/a  行政区/n]ns  同胞/n  、/wu  澳门/ns  和/c  台湾/ns  同胞/n  、/wu  海外/s  侨胞/n  ，/wd  向/p  世界/n  各国/rz  的/ud  朋友/n  们/k  ，/wd  致以/vt  诚挚/a  的/ud  问候/vn  和/c  良好/a  的/ud  祝愿/vn  ！/wt",
    "19980131-04-013-024/m  那{na4}/rz  音韵/n  如/vt  轻柔/a  的/ud  夜风/n  ，/wd  ",
    "19980103-04-003-007/m  图文/n  兼/vt  重/a  的/ud  中国/ns  文明史/n  ，/wd  就/p  方向/n  言/Vg  有利于/vt  历史学/n  和/c  考古学/n  的/ud  进一步/d  结合/vt  。/wj  考古学/n  本身/rz  是/vl  具有/vt  独立/a  的/ud  理论/n  和/c  方法/n  的/ud  学科/n  ，/wd  然而/c  中国/ns  考古学/n  从/p  一/d  开始/vt  便/d  以/p  同/p  历史学/n  的/ud  密切/ad  结合/vt  为/vl  特点/n  。/wj  大家/rr  知道/vt  ，/wd  王/nrf  国维/nrg  先生/n  二十/m  年代/n  在/p  [清华/jn  国学/n  研究院/n]nt  的/ud  讲义/n  《/wkz  古史/n  新/a  证/n  》/wky  中/f  提出/vt  的/ud  “/wyz  二/m  重/qc  证据法/n  ”/wyy  ，/wd  在/p  方法论/n  上{shang5}/f  为{wei4}/p  考古学/n  的/ud  建立/vn  发展/vn  开拓/vt  了/ul  道路/n  。/wj  “/wyz  二/m  重/qc  证据法/n  ”/wyy  指/vt  文献/n  同/p  文物/n  的/ud  互相/d  印证/vt  ，/wd  即/vl  蕴涵/vt  着/uz  历史/n  、/wu  考古/n  的/ud  结合/vn  。/wj  亲手/d  在/p  中国/ns  开展/vt  考古学/n  工作/vn  的/ud  考古学家/n  ，/wd  都/d  以/p  探索/vt  和/c  重建/vt  古史/n  为/vl  职/Ng  志/n  。/wj  最/dc  早/a  得到/vt  大规模/d  系统/ad  发掘/vt  的/ud  遗址/n  殷墟/ns  ，/wd  其/rz  被/p  选定/vt  正是/vl  出于/vt  这样/rz  的/ud  要求/n  。/wj  长期/d  领导/vt  [中国/ns  科学院/n  （/wkz  后/f  属/vl  [中国/ns  社会/n  科学院/n]nt  ）/wky  考古/vn  研究所/n]nt  的/ud  夏/nrf  鼐/nrg  先生/n  ，/wd  １９８４年/t  在/p  《/wkz  什么/ryw  是/vl  考古学/n  》/wky  文/Ng  中/f  说/vt  ，/wd  考古学/n  和/p  利用/vt  文献/n  记载/vn  进行/vx  研究/vn  的/ud  狭义/b  历史学/n  不/df  同/vt  ，/wd  研究/vt  的/ud  对象/n  只/d  是/vl  物质/n  的/ud  遗存/vn  ，/wd  但/c  两者/rz  同/d  以/p  恢复/vt  人类/n  历史/n  的/ud  本来面目/in  为/vl  目标/n  ，/wd  如/vt  车{che1}/n  之/u  两/m  轮/Ng  ，/wd  鸟/n  之/u  两翼/n  。/wj  对于/p  了解/vt  中国/ns  有着/vt  悠久/a  的/ud  文明/n  和/c  丰富/a  的/ud  文献/n  传统/n  的/ud  人们/n  来说/u  ，/wd  中国/ns  考古学/n  的/ud  这种/r  特点/n  乃是/vl  自然/a  的/ud  。/wj"
)

s = test_data[3]


def test_lexer():
    lexer.input(s)
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        print(tok.type, tok.value, tok.lineno, tok.lexpos)


def test_parser():
    parser = make_parser()
    result = parser.parse(s)

    for token in result:
        print(token.token, token.pinyin, token.pos)
