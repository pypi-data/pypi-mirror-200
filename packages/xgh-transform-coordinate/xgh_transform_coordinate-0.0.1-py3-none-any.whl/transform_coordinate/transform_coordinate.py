#!/usr/bin/env python
# coding: utf-8

# In[1]:
import os
import sys
import subprocess
import argparse
import numpy as np

import doctest

CWD = os.getcwd()
sys.path.append(CWD)


def _get_t_of_affine(origin_tri_points, destination_tri_points):
    '''
    >>> origin_tri_points = np.array(((0, 0), (4, 3), (-3, 4)))
    >>> destination_tri_points = np.array(((0, 0), (5, 0), (0, 5)))
    >>> oneline = np.array([[1], [1], [1]])
    >>> t = _get_t_of_affine(origin_tri_points, destination_tri_points)
    >>> np.allclose(t, np.array([[ 0.8,  0.6,  0], \
                                 [-0.6, 0.8, 0], \
                                 [0, 0,  1]]))
    True
    '''
    oneline = np.array([[1], [1], [1]])
    ori_m = np.append(origin_tri_points, oneline, axis=1).T
    des_m = np.append(destination_tri_points, oneline, axis=1).T
    return des_m@np.linalg.inv(ori_m)


def _rotate(v, a=np.pi/2):
    '''
    >>> fuzz = _rotate(np.array((4., 3.))) - np.array([-3., 4.])
    >>> np.min(fuzz) < 1e-6
    True
    '''
    m_rotation = np.array(((np.cos(a), -np.sin(a)), (np.sin(a), np.cos(a))))
    return m_rotation@v


def _get_perpendicular_point(two_pnts):
    '''
    >>> two_pnts = np.array([[0, 0], [4, 3]])
    >>> pp = _get_perpendicular_point(two_pnts)
    >>> np.allclose(pp, [-3, 4])
    True
    '''
    v = two_pnts[1] - two_pnts[0]
    return _rotate(v) + two_pnts[0]


def get_transform_affine_by_2pnts(origin_two_pnts, des_two_pnts):
    '''
    >>> org = np.array([[4328365.8239, 501011.8608],[4331109.5611, 500453.3748]])
    >>> des = np.array([[4000,6800],[4000,4000]])
    >>> t = get_transform_affine_by_2pnts(org, des)
    >>> org_ps, des_ps = np.append(org[0], [1]), np.append(des[0], [1])
    >>> np.allclose(t@org_ps, des_ps)
    True
    '''
    org_tri_pnts = np.concatenate(
        [origin_two_pnts, np.array([_get_perpendicular_point(origin_two_pnts)])])
    des_tri_pnts = np.concatenate(
        [des_two_pnts, np.array([_get_perpendicular_point(des_two_pnts)])])
    return _get_t_of_affine(org_tri_pnts, des_tri_pnts)


def transform_point(pt, origin_two_pnts, des_two_pnts):
    '''
    >>> org = np.array([[501011.8608, 4328365.8239],[500453.3748, 4331109.5611]])
    >>> des = np.array([[4000,6800],[4000,4000]])
    >>> pnt_i = org[0]
    >>> pnt_o = transform_point(pnt_i, org, des)
    >>> np.allclose(pnt_o, np.array([4000, 6800]))
    True
    >>> pnt_i = org[1]
    >>> pnt_o = transform_point(pnt_i, org, des)
    >>> np.allclose(pnt_o, des[1])
    True
    '''
    t = get_transform_affine_by_2pnts(origin_two_pnts, des_two_pnts)

    pt_i = np.append(pt, [1])
    return (t@pt_i)[:2]


def _format_pnt_to_str(pnt):
    return " ".join([str(i) for i in pnt] + ["0"])


def lisp_template(p0, pxaxis, pyaxis, ucs_name="\"ucs_name_\""):
    '''
    >>> lsp = lisp_template(np.array([0, 0]), np.array([1,  2]), np.array([4, 5]))
    >>> print(lsp)
    '''
    p0 = _format_pnt_to_str(p0)
    pxaxis = _format_pnt_to_str(pxaxis)
    pyaxis = _format_pnt_to_str(pyaxis)

    from string import Template

    template = Template('''
(vl-load-com)
(defun create-ucs ( / ACADOBJ CNT DOC ORIGIN UCSCOLL UCSOBJ UCS_NAME XAXISPNT YAXISPNT )
  ;; This example finds the current UserCoordinateSystems collection and
  ;; adds a new UCS to that collection.
  (setq acadObj (vlax-get-acad-object))
  (setq doc (vla-get-ActiveDocument acadObj))
  (setq UCSColl (vla-get-UserCoordinateSystems doc))
  ;; Create a UCS named "TEST" in the current drawing
  ;; Define the UCS
  (setq	origin	 (vlax-3d-point $p0)
	xAxisPnt (vlax-3d-point $pxaxis)
	yAxisPnt (vlax-3d-point $pyaxis)
  )
  ;; Add the UCS to the UserCoordinatesSystems collection
  (setq ucs_name $ucs_name)
  (setq cnt 1)
  (while (get_item UCSColl ucs_name)
    (setq ucs_name (strcat ucs_name "-("
			   (itoa cnt)
			   ")"))
    (setq cnt (1+ cnt))
    )
  (setq ucsObj (vla-Add UCSColl origin xAxisPnt yAxisPnt ucs_name))
  (print
    (strcat "A new UCS called "
	    (vla-get-Name ucsObj)
	    " has been added to the UserCoordinateSystems collection."
    )
  )
)

(defun get_item (collection name / obj)
  (if
    (not
      (vl-catch-all-error-p
        (setq obj (vl-catch-all-apply 'vla-item (list collection name)))
      )
    )
    obj
  )
)
(create-ucs)
''')
    lsp = template.substitute(p0=p0, pxaxis=pxaxis,
                              pyaxis=pyaxis, ucs_name=ucs_name)
    return lsp

# doctest.testmod()


# In[2]:


def generate_lsp_creating_ucs(org, des, lsp_name="create_usc_by_orgAnddes.lsp", ucs_name="\"WCS->LOCAL\""):
    '''
    创建一个lisp文件，在CAD文件中建立用户坐标系。
    >>> org = np.array([[501011.8608, 4328365.8239],[500453.3748, 4331109.5611]])
    >>> des = np.array([[4000,6800],[4000,4000]])
    >>> generate_lsp_creating_ucs(org, des)
    '''
    from pathlib import Path
    file_name = Path(lsp_name)

    _p0, _px, _py = [0, 0], [1000, 0], [0, 1000]
    p0 = transform_point(_p0, des, org)
    px = transform_point(_px, des, org)
    py = transform_point(_py, des, org)
    lsp = lisp_template(p0, px, py, ucs_name=ucs_name)
    t = get_transform_affine_by_2pnts(org, des)
    transform_matrix = "\n".join([";;;" + line for line in str(t).split('\n')])
    file_name.write_text(lsp+transform_matrix)


# doctest.testmod()


# In[5]:
def init_config():
    s = r'''
import numpy as np

org = np.array([[501011.8608, 4328365.8239], [500453.3748, 4331109.5611]])
des = np.array([[2800, 0], [0, 0]])
lsp_name_local="to_FUGU_local_00.lsp"
ucs_name_local="\"FUGU_LOCAL(00)\""
lsp_name_global="local_00_to_FUGU2000.lsp"
ucs_name_global="\"FUGU_2000(00)\""
        '''
    with open('config.py', 'wt', encoding='UTF8') as f:
        f.write(s)


def generate_lsp():
    import config
    org = config.org
    des = config.des

    lsp_name_local = config.lsp_name_local
    ucs_name_local = config.ucs_name_local

    lsp_name_global = config.lsp_name_global
    ucs_name_global = config.ucs_name_global
    generate_lsp_creating_ucs(
        org, des, lsp_name=lsp_name_local, ucs_name=ucs_name_local)
    generate_lsp_creating_ucs(
        des, org, lsp_name=lsp_name_global, ucs_name=ucs_name_global)


def main(argv=None):
    notexits_config = False

    try:
        import config
        print("config imported ***")
    except:
        notexits_config = True
        print("初设化配置文件config.py ...")
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', action='store_true', help="填写配置信息")
    args = parser.parse_args(argv)
    if args.config or notexits_config:
        init_config()
        subprocess.call(['powershell', 'code', 'config.py'])
        print("设置转换坐标参数...")
        return 0
    generate_lsp()
    print("生成坐标转换lsp文件 ...")


# In[ ]:


if __name__ == "__main__":
    print(CWD)
    main()
