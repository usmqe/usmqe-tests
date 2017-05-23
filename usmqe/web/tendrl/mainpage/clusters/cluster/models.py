"""
Common page model for cluster details navigation
"""


from webstr.core import WebstrModel, By, PageElement, RootPageElement


class ClusterMenuModel(WebstrModel):
    """
    Common page model for cluster details menu.
    """
    _root = RootPageElement(
        By.XPATH,
        '//*[contains(@class,"cluster-detail-nav")]')
    overview_link = PageElement(
        By.XPATH,
        './/a[contains(text(),"Overview")]')
    hosts_link = PageElement(
        By.XPATH,
        './/a[contains(text(),"Hosts")]')


class GlusterMenuModel(ClusterMenuModel):
    """
    Common page model for gluster cluster details menu.
    """
    file_shares_link = PageElement(
        By.XPATH,
        './/a[contains(text(),"File Shares")]')


class CephMenuModel(ClusterMenuModel):
    """
    Common page model for ceph cluster details menu.
    """
    pools_link = PageElement(
        By.XPATH,
        './/a[contains(text(),"Pools")]')
    rbds_link = PageElement(
        By.XPATH,
        './/a[contains(text(),"RBDs")]')
